from unittest.mock import patch, Mock, ANY

from src.main import commit_msg_hook as sut
from src.main.hook.commit_msg_hook_runner import ExitCode
from src.test.base_unit_test import BaseUnitTest


# Main will not run without the correct __name__
@patch("src.main.commit_msg_hook.__name__", "__main__")
class TestCommitMsgHook(BaseUnitTest.BaseTestCase):
    mock_hook_runner: Mock
    mock_sys: Mock
    mock_os: Mock
    SUT_PATCH: str = "src.main.commit_msg_hook"

    def setUp(self):
        self.mock_hook_runner = self.create_patch(self.SUT_PATCH + ".CommitMessageHookRunner")
        # Default return code SUCCESS
        self.mock_hook_runner.return_value.run.return_value = ExitCode.SUCCESS
        self.mock_sys = self.create_patch(self.SUT_PATCH + ".sys")
        self.mock_os = self.create_patch(self.SUT_PATCH + ".os")

    def test_incorrect_prod_command_line_args(self):
        # Setup an array with one too many arguments
        self.mock_sys.argv = ["arg"] * (sut.NUM_PROD_ARGUMENTS_EXPECTED + 1)
        sut.main()
        self.mock_sys.exit.assert_called_once_with(ExitCode.FAILURE.value)

    def test_incorrect_debug_command_line_args(self):
        self.mock_sys.argv = ['Dummy path', sut.DEBUG_FLAG]
        sut.main()
        self.mock_sys.exit.assert_called_once_with(ExitCode.FAILURE.value)

    def test_correct_debug_command_line_args(self):
        self.mock_sys.argv = ['Dummy path', sut.DEBUG_FLAG, "X", "Y"]
        sut.main()
        self.mock_sys.exit.assert_called_once_with(ExitCode.SUCCESS.value)
        self.mock_hook_runner.assert_called_once_with("X", "Y", ANY)

    def test_correct_prod_command_line_args(self):
        self.mock_os.getcwd.return_value = "test_value"
        self.mock_sys.argv = ['Dummy path', "VALUE"]
        sut.main()
        self.mock_sys.exit.assert_called_once_with(ExitCode.SUCCESS.value)
        self.mock_hook_runner.assert_called_once_with("test_value", "VALUE", ANY)

    def test_no_command_line_args(self):
        self.mock_sys.argv = []
        sut.main()
        self.mock_sys.exit.assert_called_once_with(ExitCode.FAILURE.value)
        self.mock_hook_runner.assert_not_called()
