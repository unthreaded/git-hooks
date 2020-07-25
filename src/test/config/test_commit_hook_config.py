import os
import unittest

from src.main.config.commit_hook_config import CommitHookConfig
from src.main.config.commit_hook_config_base_impl import CommitHookConfigDefaultImpl
from src.main.config.commit_hook_config_ini_impl import CommitHookConfigINIImpl


class TestBaseImplCommitHookConfig(unittest.TestCase):
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

    def test_issue_url_prefix(self):
        self.assertIsNotNone(self.sut.get_issue_url_prefix(), msg="Should return issue URL prefix")


class TestINIImplCommitHookConfig(unittest.TestCase):
    sut: CommitHookConfig = None

    def setUp(self):
        super().setUp()
        self.sut = CommitHookConfigINIImpl(
            open(os.path.join("src", "main", CommitHookConfigINIImpl.CONFIG_FILE_NAME), 'r')
        )

    def test_protected_branch_prefixes(self):
        self.assertListEqual(
            self.sut.get_protected_branch_prefixes(), ['release', 'dev', 'hotfix'],
            "Branch prefixes don't match"
        )

    def test_get_issue_pattern(self):
        self.assertEqual(
            self.sut.get_issue_pattern(),
            'GH-[0-9]+',
            msg="Found incorrect issue pattern")

    def test_get_no_issue_phrase(self):
        self.assertEqual(
            self.sut.get_no_issue_phrase(),
            'NOGH',
            msg="Found incorrect no issue phrase")

    def test_issue_url_prefix(self):
        self.assertEqual(
            self.sut.get_issue_url_prefix(),
            'https://github.com/unthreaded/git-hooks/issues/',
            msg="Found incorrect issue URL prefix")

    def test_exception_raised_with_null_file(self):
        # We expect Exception class to be thrown when
        # we call the config impl constructor with an argument of None
        self.assertRaises(Exception, CommitHookConfigINIImpl, None)
