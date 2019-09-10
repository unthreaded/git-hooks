import unittest
from unittest.mock import patch, Mock
from src.main import commit_msg_hook


class TestCommitMsgHook(unittest.TestCase):
    def test_incorrect_command_line_args(self):
        """
            When we receive the incorrect number of command line arguments,
             we should exit with FAILURE
        """

        # Setup an array with one too many arguments
        mock_args = ["arg"] * (commit_msg_hook.NUM_ARGUMENTS_EXPECTED + 1)

        with patch("sys.argv", mock_args):
            with patch.object(commit_msg_hook, "__name__", "__main__"):
                mock_exit = Mock(name="exit")
                commit_msg_hook.exit = mock_exit
                commit_msg_hook.main()

                mock_exit.assert_called_once_with(commit_msg_hook.ExitCodes.FAILURE)
