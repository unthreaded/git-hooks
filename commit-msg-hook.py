import os
from pygit2 import Repository

def commit_msg():
    branch = Repository('.').head.shorthand
    branchNoDir = branch.rsplit("/",1)[-1]
    print(branchNoDir)

commit_msg()