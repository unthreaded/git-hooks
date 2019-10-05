"""
    This file handles finding a ticket number and placing it into the commit message
"""
import logging
import os
import re
from enum import Enum

from pygit2 import Repository

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

    def run(self) -> ExitCode:
        """
                Add the ticket to the git commit message if possible
        """
        issue = self.hook_config.get_no_issue_phrase()
        is_commit_compliant = True
        is_branch_non_compliant = False
        issue_pattern: str = self.hook_config.get_issue_pattern()

        repo = Repository(self.git_repo_path)
        branch_name = repo.head.name

        commit_msg_file_path: str = os.path.join(self.git_repo_path, self.git_commit_message_path)
        commit_msg_text = open(commit_msg_file_path, 'r').read()

        lower_commit_text = commit_msg_text.lower()
        if lower_commit_text.startswith("revert") or lower_commit_text.startswith("merge"):
            logging.info("Merging or Reverting, will not change commit message.")
            return ExitCode.SUCCESS

        for protected_branch_prefix in self.hook_config.get_protected_branch_prefixes():
            if re.search(protected_branch_prefix,
                         branch_name,
                         re.IGNORECASE):
                logging.error("You just committed to an exempt branch! ( %s )", branch_name)
                return ExitCode.SUCCESS

        if not any(re.findall(issue_pattern + ": .*", commit_msg_text)):
            is_commit_compliant = False

        if not get_left_most_issue_in_string(issue_pattern, branch_name):
            is_branch_non_compliant = True

        if is_branch_non_compliant and (not is_commit_compliant):
            logging.info("Cannot find ticket in branch name, assuming NOGH: %s", branch_name)
        else:
            issue = re.findall(issue_pattern, branch_name)[0]

        if is_commit_compliant:
            commit_issue = re.findall(issue_pattern, commit_msg_text)[0]
            if issue != commit_issue:
                logging.info(
                    "GH issue in commit does not match branch (%s != %s), will not rewrite commit.",
                    commit_issue,
                    issue)
                return ExitCode.SUCCESS
            return ExitCode.SUCCESS

        issue_num = get_left_most_issue_in_string(issue_pattern, branch_name)
        commit_msg_text = "%s: %s" % (issue, commit_msg_text)
        if issue != self.hook_config.get_no_issue_phrase():
            issue = self.hook_config.get_issue_url_prefix() + issue_num
        logging.info("Rewriting commit to use issue: %s", issue)

        # Open file for write, which will empty the file contents
        commit_msg_file = open(commit_msg_file_path, 'w')
        commit_msg_file.write(commit_msg_text)
        commit_msg_file.close()
        return ExitCode.SUCCESS
