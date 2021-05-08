"""
    This file handles finding a ticket number and placing it into the commit message
"""
import logging
import os
import re
import subprocess
from enum import Enum

from src.main.config.commit_hook_config import CommitHookConfig


class ExitCode(Enum):
    """
        Simple class for consistent exit codes
    """
    SUCCESS = 0
    FAILURE = -1


def get_left_most_issue_in_string(issue_pattern: str, string: str) -> str:
    """
        >>> get_left_most_issue_in_string("GH-[0-9]+", "feature/GH-123-some-story-or-bug")
        'GH-123'
        >>> get_left_most_issue_in_string("GH-[0-9]+", "feature/GH-456-GH-789-some-story-or-bug")
        'GH-456'
        >>> get_left_most_issue_in_string("GH-[0-9]+", "feature/gh-456-GH-789-some-story-or-bug")
        'gh-456'
        >>> get_left_most_issue_in_string("GH-[0-9]+", "dummy-branch-without_issue") is None
        True
        >>> get_left_most_issue_in_string("ISSUE-[0-9]+", "ISSUE-ISSUE-1234-new-feature")
        'ISSUE-1234'
        >>> get_left_most_issue_in_string("NOGH", "NOGH | whatever")
        'NOGH'
        >>> get_left_most_issue_in_string("NOGH", " NOGH: whatever")
        'NOGH'
        >>> get_left_most_issue_in_string("TICKET-[0-9]+|NOGH", "NOGH: something for TICKET-123")
        'NOGH'
    """
    result = re.search(issue_pattern, string, re.IGNORECASE)
    if result:
        return result.group()
    return None


class CommitMessageHookRunner:
    """
        This class is the main functionality of the hook
    """
    git_repo_path: str
    git_commit_message_path: str
    hook_config: CommitHookConfig

    def __init__(self, git_repo_path: str, git_commit_message_path: str, config: CommitHookConfig):
        self.git_repo_path = git_repo_path
        self.git_commit_message_path = git_commit_message_path
        self.hook_config = config

    def get_current_branch_name(self) -> str:
        """
        :return: Current branch checked out in repo
        """
        branch_name = subprocess.check_output(
            "git branch --show-current".split(),
            cwd=self.git_repo_path
        )
        return branch_name.strip().decode("utf-8")

    def run(self) -> ExitCode:
        """
                Add the ticket to the git commit message if possible
        """
        issue_pattern: str = self.hook_config.get_issue_pattern()
        issue_or_no_issue_pattern: str = \
            "%s|%s" % (issue_pattern, self.hook_config.get_no_issue_phrase())

        branch_name: str = self.get_current_branch_name()

        commit_msg_file_path: str = os.path.join(self.git_repo_path, self.git_commit_message_path)
        raw_commit_msg_text: str = open(commit_msg_file_path, 'r').read()
        commit_msg_text: str = raw_commit_msg_text.splitlines()[0]

        issue_in_branch: str = get_left_most_issue_in_string(issue_pattern, branch_name)
        issue_in_commit: str = get_left_most_issue_in_string(issue_or_no_issue_pattern,
                                                             commit_msg_text)

        lower_commit_text = commit_msg_text.lower()
        if lower_commit_text.startswith("revert") or lower_commit_text.startswith("merge"):
            logging.info("Merging or Reverting, will not change commit message.")
            return ExitCode.SUCCESS

        for protected_branch_prefix in self.hook_config.get_protected_branch_prefixes():
            if re.search(f"^{protected_branch_prefix}",
                         branch_name,
                         re.IGNORECASE):
                logging.error("You just committed to an exempt branch! ( %s )", branch_name)
                return ExitCode.FAILURE

        # A commit that already has an issue is okay,
        # we just warn the user if it doesn't match the issue in the branch.
        if issue_in_commit:
            if issue_in_branch and issue_in_commit != issue_in_branch:
                logging.info(
                    "Issue in commit does not match branch (%s != %s), will not rewrite commit.",
                    issue_in_commit,
                    issue_in_branch)
            return ExitCode.SUCCESS

        if issue_in_branch:
            logging.info("Rewriting commit to use issue: %s%s",
                         self.hook_config.get_issue_url_format(),
                         issue_in_branch)
        else:
            issue_in_branch = self.hook_config.get_no_issue_phrase()
            logging.info(
                "Cannot find ticket in branch name, assuming %s: %s",
                issue_in_branch,
                branch_name)

        commit_msg_text = "%s: %s" % (issue_in_branch, raw_commit_msg_text)

        # Open file for write, which will empty the file contents
        commit_msg_file = open(commit_msg_file_path, 'w')
        commit_msg_file.write(commit_msg_text)
        commit_msg_file.close()

        return ExitCode.SUCCESS
