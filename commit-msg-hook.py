from __future__ import print_function
import sys
import re

def commit_msg():
    BRANCH = sys.argv[1]
    COMMIT_MSG = sys.argv[2]
    GH_ISSUE_URL = sys.argv[3]
    EXEMPTION_KEYWORDS = "^Merge|^Revert"
    PROTECTED_BRANCHES = "^dev|^release.*|^hotfix.*"
    BRANCH_NO_DIR = BRANCH.rsplit("/", 1)[-1]
    ISSUE_PATTERN = "GH-[0-9]+|NOGH"
    NO_TICKET_KEYWORD = "NOGH"
    ISSUE = NO_TICKET_KEYWORD

    isCommitCompliant = True
    isBranchNonCompliant = False

    if any(re.findall(EXEMPTION_KEYWORDS, COMMIT_MSG, re.IGNORECASE)):
        print("Merging or Reverting, will not change commit message.")
        exit(0)

    if any(re.findall(PROTECTED_BRANCHES, BRANCH, re.IGNORECASE)):
        print("You just committed to an exempt branch! " + BRANCH)
        exit(1)

    commit_pattern = ISSUE_PATTERN + ": .*"
    if not any(re.findall(commit_pattern, COMMIT_MSG)):
        isCommitCompliant = False

    if not any(re.findall(ISSUE_PATTERN, BRANCH_NO_DIR)):
        isBranchNonCompliant = True

    if (isBranchNonCompliant and (not isCommitCompliant)):
        print("Cannot find ticket in branch name, assuming NOGH: " + BRANCH)
    else:
        ISSUE = re.findall(ISSUE_PATTERN, BRANCH_NO_DIR)[0]

    if isCommitCompliant:
        commit_issue = re.findall(ISSUE_PATTERN, COMMIT_MSG)[0]
        if (ISSUE != commit_issue):
            print("GH issue in commit does not match branch (%s != %s), will not rewrite commit."
                  % (commit_issue, ISSUE))
            exit(0)
        exit(0)

    issue_num = re.findall(r'[0-9]+', ISSUE)[0]
    final_commit_msg = "%s: %s" % (ISSUE, COMMIT_MSG)
    if ISSUE != NO_TICKET_KEYWORD:
        ISSUE = "%s%s" % (GH_ISSUE_URL, issue_num)
    print("Rewriting commit to use issue: %s" % ISSUE, file=sys.stderr)
    print(final_commit_msg)
    exit(0)

commit_msg()