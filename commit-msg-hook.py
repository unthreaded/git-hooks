from __future__ import print_function

import logging
import os
import re
import sys


def commit_msg():
    BRANCH = sys.argv[1]
    COMMIT_MSG = sys.argv[2]
    GH_ISSUE_URL = sys.argv[3]
    EXEMPTION_KEYWORDS = "^Merge|^Revert"
    PROTECTED_BRANCHES = "^dev|^release.*|^hotfix.*"
    BRANCH_NO_DIR = BRANCH.rsplit("/", 1)[-1]
    ISSUE_PATTERN = "GH-[0-9]+|NOGH"
    NO_TICKET_KEYWORD = "NOGH"

    issue = NO_TICKET_KEYWORD
    isCommitCompliant = True
    isBranchNonCompliant = False

    if any(re.findall(EXEMPTION_KEYWORDS, COMMIT_MSG, re.IGNORECASE)):
        logging.info("Merging or Reverting, will not change commit message.")
        exit(0)

    if any(re.findall(PROTECTED_BRANCHES, BRANCH, re.IGNORECASE)):
        logging.error("You just committed to an exempt branch! " + BRANCH)
        exit(1)

    commit_pattern = ISSUE_PATTERN + ": .*"
    if not any(re.findall(commit_pattern, COMMIT_MSG)):
        isCommitCompliant = False

    if not any(re.findall(ISSUE_PATTERN, BRANCH_NO_DIR)):
        isBranchNonCompliant = True

    if isBranchNonCompliant and (not isCommitCompliant):
        logging.info("Cannot find ticket in branch name, assuming NOGH: " + BRANCH)
    else:
        issue = re.findall(ISSUE_PATTERN, BRANCH_NO_DIR)[0]

    if isCommitCompliant:
        commit_issue = re.findall(ISSUE_PATTERN, COMMIT_MSG)[0]
        if issue != commit_issue:
            logging.info("GH issue in commit does not match branch (%s != %s), will not rewrite commit."
                         % (commit_issue, issue))
            exit(0)
        exit(0)

    issue_num = re.findall(r'[0-9]+', issue)[0]
    final_commit_msg = "%s: %s" % (issue, COMMIT_MSG)
    if issue != NO_TICKET_KEYWORD:
        issue = "%s%s" % (GH_ISSUE_URL, issue_num)
    logging.info("Rewriting commit to use issue: %s" % issue)

    p = os.path.join('.git', 'COMMIT_EDITMSG')
    with open(p, "w") as f:
        f.write(final_commit_msg)
    exit(0)


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    commit_msg()


main()
