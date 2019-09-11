"""
    This file handles command line arguments and invoking the hook
"""

import logging
import sys

from src.main.config.commit_hook_config_base_impl import CommitHookConfigDefaultImpl
from src.main.hook.commit_msg_hook_runner import CommitMessageHookRunner, ExitCode

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
            exit(ExitCode.FAILURE)
        else:
            git_repo_path: str = sys.argv[0]
            git_commit_msg_file_name: str = sys.argv[1]
            exit(
                CommitMessageHookRunner(
                    git_repo_path,
                    git_commit_msg_file_name,
                    CommitHookConfigDefaultImpl()
                ).run()
            )


main()
