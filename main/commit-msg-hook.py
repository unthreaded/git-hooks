from pygit2 import Repository


def commit_msg():
    print(Repository('.').head.shorthand)


commit_msg()
