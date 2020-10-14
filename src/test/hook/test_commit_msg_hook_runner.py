from typing import List
from unittest.mock import Mock, MagicMock

from src.main.config.commit_hook_config import CommitHookConfig
from src.main.hook.commit_msg_hook_runner import CommitMessageHookRunner, ExitCode
from src.test.base_unit_test import BaseUnitTest


class TestCommitMessageRunner(BaseUnitTest.BaseTestCase):
    sut: CommitMessageHookRunner = None

    repo_path = "/example/whatever/folder/path/"
    commit_msg_path = ".git/COMMIT_MSG"
    config: CommitHookConfig = MagicMock(spec=CommitHookConfig)
    message_written_to_commit_file: str
    mock_commit_file: Mock
    mock_repo: MagicMock
    mock_logging: Mock
    SUT_PATCH: str = "src.main.hook.commit_msg_hook_runner"

    def set_detached_head_flag(self, boolean: bool):
        self.mock_repo.return_value.head_is_detached = boolean

    def set_unborn_head_flag(self, boolean: bool):
        self.mock_repo.return_value.head_is_unborn = boolean

    def set_protected_branches(self, branches: List[str]):
        self.config.get_protected_branch_prefixes.return_value = branches

    def setUp(self):
        self.sut = CommitMessageHookRunner(self.repo_path, self.commit_msg_path, self.config)
        self.message_written_to_commit_file = None

        self.mock_commit_file = MagicMock(autospec=True)

        def write_to_commit_file(value: str):
            self.message_written_to_commit_file = value

        self.mock_commit_file.write = Mock(side_effect=write_to_commit_file)

        self.mock_open = self.create_patch('builtins.open')
        self.mock_open.return_value = self.mock_commit_file
        self.mock_repo = self.create_patch(self.SUT_PATCH + ".Repository")
        self.mock_logging = self.create_patch(self.SUT_PATCH + ".logging")
        self.set_unborn_head_flag(False)
        self.set_detached_head_flag(False)

        # Setup config information
        self.config.get_issue_pattern.return_value = "TICKET-[0-9]+"
        self.set_protected_branches([])
        self.config.get_issue_url_format.return_value = "com.whatever/"
        self.config.get_no_issue_phrase.return_value = "NOTICKET"

        # Setup dummy git environment
        self.set_branch_name("feature/TICKET-1234-new-feature")
        self.set_commit_message("""Example commit text
        # example comment from get about feature/TICKET-123-whatever
        # example comment 2 about NOTICKET
        """)

    def set_commit_message(self, message: str):
        self.mock_commit_file.read.return_value = message

    def set_branch_name(self, branch: str):
        self.mock_repo.return_value.head.name = branch

    def assert_n_calls_made_to_logging(self, num_calls: int):
        self.assertEqual(
            num_calls,
            len(self.mock_logging.method_calls),
            "Incorrect num calls made to logging")

    def test_no_action_taken_on_merge_or_revert(self):
        no_action_commit_messages = ["revert changes from release/V1.2",
                                     "MERGE changes from release/V1.2"]

        for no_action_commit in no_action_commit_messages:
            print("Testing this commit message: %s" % no_action_commit)

            self.set_commit_message(no_action_commit)

            self.sut.run()
            self.assertIsNone(self.message_written_to_commit_file,
                              "Nothing should have been written to the commit file")

            self.assert_n_calls_made_to_logging(1)

            # Start fresh for next run
            self.setUp()

    def test_issue_written_to_commit_from_branch_name(self):
        self.sut.run()

        self.assertIsNotNone(self.message_written_to_commit_file,
                             "Nothing was written to commit file")
        self.assertTrue(self.message_written_to_commit_file.startswith("TICKET-1234"),
                        "The ticket was not added to the start of the commit message")
        self.assert_n_calls_made_to_logging(1)

    def test_that_nothing_happens_when_issue_is_already_in_commit(self):
        commits_that_should_not_be_edited = [
            "NOTICKET: I changed stuff",
            "TICKET-1234 | I changed stuff"
        ]

        self.set_branch_name("something")

        for commit_message in commits_that_should_not_be_edited:
            self.set_commit_message(commit_message)

            self.sut.run()

            self.assertIsNone(self.message_written_to_commit_file,
                              "Nothing should have been written to commit file")

            self.assert_n_calls_made_to_logging(0)

            # Start fresh next time
            self.setUp()

    def test_warning_on_non_matching_issue_numbers(self):
        self.set_branch_name("feature/TICKET-123")
        self.set_commit_message("NOTICKET blah blah blah")

        self.sut.run()

        self.assertIsNone(self.message_written_to_commit_file,
                          "Nothing should have been written to commit file")

        self.assert_n_calls_made_to_logging(1)

    def test_default_issue_going_to_commit_message(self):
        self.set_branch_name("no-issue-here")
        self.set_commit_message("blah blah blah")

        self.sut.run()

        self.assert_n_calls_made_to_logging(1)

        self.assertTrue(
            self.message_written_to_commit_file.startswith(self.config.get_no_issue_phrase()),
            "The NO ISSUE ticket was not added to the start of the commit message")

    def test_no_changes_to_exempt_branches(self):
        self.set_protected_branches(["release"])
        self.set_branch_name("release/version-one")
        self.set_commit_message("blah blah blah")

        self.sut.run()

        self.assertIsNone(self.message_written_to_commit_file,
                          "Nothing should have been written to commit file")

        self.assert_n_calls_made_to_logging(1)

    def test_detached_head_returns_empty_branch(self):
        self.set_detached_head_flag(True)
        self.assertEqual("", self.sut.get_current_branch_name())

    def test_unborn_head_returns_empty_branch(self):
        self.set_unborn_head_flag(True)
        self.assertEqual("", self.sut.get_current_branch_name())

    def test_exit_failure_on_protected_branch(self):
        self.set_protected_branches(['master'])
        self.set_branch_name('master')
        self.assertEqual(self.sut.run().value, ExitCode.FAILURE.value)

    def test_protected_branch_edge_case_does_not_cause_failure(self):
        self.set_protected_branches(['dev'])
        self.set_branch_name('feature/start-dev-for-amazing-new-stuff')
        self.assertEqual(self.sut.run().value, ExitCode.SUCCESS.value,
                         "Protected branch should only invoke if current branch"
                         " begins with prefix, not if contained in current branch")
