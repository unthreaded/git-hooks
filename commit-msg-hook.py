from pygit2 import Repository
from git import Repo

def commit_msg():
    BRANCH = Repository('.').head.shorthand
    BRANCH_NO_DIR = BRANCH.rsplit("/",1)[-1]
    ISSUE_PATTERN="GH-[0-9]+"
    TICKET_BASE_URL="https://github.com/unthreaded/issues/"
    NO_TICKET_KEYWORD="NOGH"

    #TODO: add logic for commit-msg

commit_msg()