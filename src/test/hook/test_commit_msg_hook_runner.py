from unittest.mock import Mock, MagicMock

from src.main.config.commit_hook_config import CommitHookConfig
from src.main.hook.commit_msg_hook_runner import CommitMessageHookRunner
from src.test.base_unit_test import BaseUnitTest


class TestCommitMessageRunner(BaseUnitTest.BaseTestCase):
    sut: CommitMessageHookRunner = None

    repo_path = "/example/whatever/folder/path/"
    commit_msg_path = ".git/COMMIT_MSG"
    config: CommitHookConfig = MagicMock(spec=CommitHookConfig)
    message_written_to_commit_file: str
    mock_commit_file: Mock
    mock_repo: MagicMock

    def setUp(self):
        self.sut = CommitMessageHookRunner(self.repo_path, self.commit_msg_path, self.config)
        self.message_written_to_commit_file = None

        self.mock_commit_file = MagicMock(autospec=True)

        def write_to_commit_file(value: str):
            self.message_written_to_commit_file = value

        self.mock_commit_file.write = Mock(side_effect=write_to_commit_file)

        self.mock_open = self.create_patch('builtins.open')
        self.mock_open.return_value = self.mock_commit_file
        self.mock_repo = self.create_patch("src.main.hook.commit_msg_hook_runner.Repository")

        # Setup config information
        self.config.get_issue_pattern.return_value = "TICKET-[0-9]+"
        self.config.get_protected_branch_prefixes.return_value = []
        self.config.get_issue_url_prefix.return_value = "com.whatever/"
        self.config.get_no_issue_phrase.return_value = "NOTICKET"

        # Setup dummy git environment
        self.set_branch_name("feature/TICKET-1234-new-feature")
        self.set_commit_message("Example commit text")

    def set_commit_message(self, message: str):
        self.mock_commit_file.read.return_value = message

    def set_branch_name(self, branch: str):
        self.mock_repo.return_value.head.name = branch

    def test_no_action_taken_on_merge_or_revert(self):
        no_action_commit_messages = ["revert changes from release/V1.2",
                                     "MERGE changes from release/V1.2"]

        for no_action_commit in no_action_commit_messages:
            print("Testing this commit message: %s" % no_action_commit)

            self.set_commit_message(no_action_commit)

            self.sut.run()
            self.assertIsNone(self.message_written_to_commit_file,
                              "Nothing should have been written to the commit file")

            # Start fresh for next run
            self.setUp()

    def test_issue_written_to_commit_from_branch_name(self):
        self.sut.run()

        self.assertIsNotNone(self.message_written_to_commit_file,
                             "Nothing was written to commit file")
        self.assertTrue(self.message_written_to_commit_file.startswith("TICKET-1234"),
                        "The ticket was not added to the start of the commit message")

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

            # Start fresh next time
            self.setUp()
