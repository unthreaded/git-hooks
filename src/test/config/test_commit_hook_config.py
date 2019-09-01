import unittest

from src.main.config.commit_hook_config import CommitHookConfig
from src.main.config.commit_hook_config_base_impl import CommitHookConfigDefaultImpl


class TestCommitHookConfig(unittest.TestCase):
    sut: CommitHookConfig = None

    def setUp(self):
        super().setUp()
        self.sut = CommitHookConfigDefaultImpl()

    def test_protected_branch_prefixes(self):
        val = self.sut.get_protected_branch_prefixes()
        self.assertIsNotNone(val, msg="Should return an empty list, not NONE")
        self.assertIsInstance(val, list, msg="Should be an instance of a list")

    def test_get_issue_pattern(self):
        self.assertIsNotNone(self.sut.get_issue_pattern(), msg="Should return an issue pattern")

    def test_get_no_issue_phrase(self):
        self.assertIsNotNone(self.sut.get_no_issue_phrase(), msg="Should return a no issue phrase")
