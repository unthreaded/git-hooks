"""
    This file handles command line arguments and invoking the hook
"""

import logging
import os
import sys

from src.main.config.commit_hook_config import CommitHookConfig
from src.main.config.commit_hook_config_base_impl import CommitHookConfigDefaultImpl
from src.main.config.commit_hook_config_ini_impl import CommitHookConfigINIImpl
from src.main.hook.commit_msg_hook_runner import CommitMessageHookRunner, ExitCode

NUM_PROD_ARGUMENTS_EXPECTED: int = 2
NUM_DEBUG_ARGUMENTS_EXPECTED: int = 4
DEBUG_FLAG: str = "--debug"


def get_config() -> CommitHookConfig:
    """
        Determine which config implementation to use
    :return: CommitHookConfig instance
    """
    # Command line args contain our current script/exe path
    my_exe_path: str = sys.argv[0]
    my_exe_dir = os.path.dirname(my_exe_path)
    my_exe_dir = os.path.abspath(my_exe_dir)
    config_file_path = os.path.join(my_exe_dir, CommitHookConfigINIImpl.CONFIG_FILE_NAME)

    if os.path.isfile(config_file_path):
        return CommitHookConfigINIImpl(
            open(
                config_file_path,
                'r')
        )

    logging.info(
        "Using default config, configuration not found: \n%s",
        config_file_path)
    return CommitHookConfigDefaultImpl()


def exit_invalid_num_command_line_arguments(expected: int):
    """
        Exit app if wrong # CLI arguments received
    """
    logging.error("Excepted %s arguments but got %s",
                  expected,
                  len(sys.argv))
    sys.exit(ExitCode.FAILURE.value)


def main():
    """
        Everything starts here!
        Setup as a separate function for testing purposes.

        While this code is in PROD:
            git repo: the current working directory
            commit msg file: argv[1] -- passed in from git

        While you're debugging:
            Pass in --debug as argv[1]
            git repo: argv[2]
            commit msg file: argv[3]

            example PyCharm parameters:
                > --debug C:\\Users\\Lucas\\example_repo .git\\COMMIT_EDITMSG
    """
    if __name__ == "__main__":
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

        num_command_line_args: int = len(sys.argv)
        debug_mode: bool = False
        if num_command_line_args <= 1:
            exit_invalid_num_command_line_arguments(NUM_PROD_ARGUMENTS_EXPECTED)
            return

        if sys.argv[1].lower() == DEBUG_FLAG:
            debug_mode = True
            logging.warning("Running in debug mode***")

        num_args_expected: int = \
            NUM_DEBUG_ARGUMENTS_EXPECTED if debug_mode else NUM_PROD_ARGUMENTS_EXPECTED

        if num_command_line_args != num_args_expected:
            exit_invalid_num_command_line_arguments(num_args_expected)
            return

        git_repo_path: str
        git_commit_msg_file_name: str

        if debug_mode:
            git_repo_path = sys.argv[2]
            git_commit_msg_file_name = sys.argv[3]
        else:
            git_repo_path = os.getcwd()
            git_commit_msg_file_name = sys.argv[1]

        sys.exit(
            CommitMessageHookRunner(
                git_repo_path,
                git_commit_msg_file_name,
                get_config()
            ).run().value
        )


main()
