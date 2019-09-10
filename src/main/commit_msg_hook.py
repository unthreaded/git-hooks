"""
    This file handles finding a ticket number and placing it into the commit message
"""
from __future__ import print_function

import logging
import os
import re
import sys
from enum import Enum

from pygit2 import Repository

from src.main.config.commit_hook_config import CommitHookConfig
from src.main.config.commit_hook_config_base_impl import CommitHookConfigDefaultImpl


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


def commit_msg(git_repo_path: str, git_commit_message_path: str):
    """
        Add the ticket to the git commit message if possible
    """
    config: CommitHookConfig = CommitHookConfigDefaultImpl()

    issue = config.get_no_issue_phrase()
    is_commit_compliant = True
    is_branch_non_compliant = False

    repo = Repository(git_repo_path)
    branch_name = repo.head.name
    commit_msg_file = open(os.path.join(git_repo_path, git_commit_message_path), 'w')
    commit_msg_text = commit_msg_file.read()

    if any(re.findall(config.get_protected_branch_prefixes(), commit_msg_text, re.IGNORECASE)):
        logging.info("Merging or Reverting, will not change commit message.")
        exit(0)

    if any(re.findall(config.get_protected_branch_prefixes(), branch_name, re.IGNORECASE)):
        logging.error("You just committed to an exempt branch! ( %s )", branch_name)
        exit(1)

    ticket_pattern = config.get_issue_pattern()
    if not any(re.findall(ticket_pattern + ": .*", commit_msg_text)):
        is_commit_compliant = False

    if not any(re.findall(ticket_pattern, branch_name)):
        is_branch_non_compliant = True

    if is_branch_non_compliant and (not is_commit_compliant):
        logging.info("Cannot find ticket in branch name, assuming NOGH: %s", branch_name)
    else:
        issue = re.findall(ticket_pattern, branch_name)[0]

    if is_commit_compliant:
        commit_issue = re.findall(ticket_pattern, commit_msg_text)[0]
        if issue != commit_issue:
            logging.info(
                "GH issue in commit does not match branch (%s != %s), will not rewrite commit.",
                commit_issue,
                issue)
            exit(0)
        exit(0)

    issue_num = re.findall('[0-9]+', issue)[0]
    final_commit_msg = "%s: %s" % (issue, commit_msg_text)
    if issue != config.get_no_issue_phrase():
        issue = config.get_issue_url_prefix() + issue_num
    logging.info("Rewriting commit to use issue: %s", issue)

    commit_msg_file.write(final_commit_msg)
    commit_msg_file.close()
    exit(0)


class ExitCodes(Enum):
    """
        Simple method class for consistent exit codes
    """
    SUCCESS = 0
    FAILURE = -1

NUM_ARGUMENTS_EXPECTED: int = 2


def main():
    """
        Everything starts here!
        Setup as a separate function for testing purposes.
    """
    if __name__ == "__main__":
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        num_command_line_args: int = len(sys.argv)
        if num_command_line_args != NUM_ARGUMENTS_EXPECTED:
            logging.error("Excepted %s arguments but got %s",
                          NUM_ARGUMENTS_EXPECTED,
                          num_command_line_args)
            exit(ExitCodes.FAILURE)
        else:
            git_repo_path: str = sys.argv[0]
            git_commit_msg_file_name: str = sys.argv[1]
            commit_msg(git_repo_path, git_commit_msg_file_name)


main()
