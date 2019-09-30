import unittest
from unittest.mock import Mock, patch, MagicMock

from src.main.config.commit_hook_config import CommitHookConfig
from src.main.hook.commit_msg_hook_runner import CommitMessageHookRunner


class TestCommitMessageRunner(unittest.TestCase):
    sut: CommitMessageHookRunner = None

    repo_path = "/example/whatever/folder/path/"
    commit_msg_path = ".git/COMMIT_MSG"
    config: CommitHookConfig = MagicMock(spec=CommitHookConfig)
    message_written_to_commit_file: str = None
    mock_commit_file: Mock
    mock_repo: MagicMock

    def create_patch(self, name: str):
        patcher = patch(name)
        mock_value = patcher.start()
        self.addCleanup(patcher.stop)
        return mock_value

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

    def test_no_action_taken_on_merge_or_revert(self):
        # Setup config information
        self.config.get_issue_pattern.return_value = "TICKET-[0-9]+"
        self.config.get_protected_branch_prefixes.return_value = []
        self.config.get_issue_url_prefix.return_value = "com.whatever/"

        no_action_commit_messages = ["revert changes from release/V1.2",
                                     "MERGE changes from release/V1.2"]

        for no_action_commit in no_action_commit_messages:
            print("Testing this commit message: %s" % no_action_commit)
            # Current commit contents
            self.mock_commit_file.read.return_value = no_action_commit

            self.sut.run()
            self.assertIsNone(self.message_written_to_commit_file,
                              "Nothing should have been written to the commit file")

    def test_issue_written_to_commit_from_branch_name(self):
        # Setup config information
        self.config.get_issue_pattern.return_value = "TICKET-[0-9]+"
        self.config.get_protected_branch_prefixes.return_value = []
        self.config.get_issue_url_prefix.return_value = "com.whatever/"

        # Set current branch name
        self.mock_repo.return_value.head.name = "feature/TICKET-1234-new-feature"

        # Current commit contents
        self.mock_commit_file.read.return_value = "Example commit text"

        self.sut.run()

        self.assertTrue(self.message_written_to_commit_file,
                        "Nothing was written to commit file")
        self.assertTrue(self.message_written_to_commit_file.startswith("TICKET-1234"),
                        "The ticket was not added to the start of the commit message")
