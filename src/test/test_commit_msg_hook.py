from unittest.mock import patch, Mock, ANY, MagicMock

from src.main import commit_msg_hook as sut
from src.main.config.commit_hook_config import CommitHookConfig
from src.main.hook.commit_msg_hook_runner import ExitCode
from src.test.base_unit_test import BaseUnitTest


# Main will not run without the correct __name__
@patch("src.main.commit_msg_hook.__name__", "__main__")
class TestCommitMsgHook(BaseUnitTest.BaseTestCase):
    mock_hook_runner: Mock
    mock_sys: Mock
    mock_os: Mock
    mock_yaml_config: Mock
    mock_default_config: Mock
    mock_logging: Mock
    SUT_PATCH: str = "src.main.commit_msg_hook"

    def setUp(self):
        self.mock_hook_runner = self.create_patch(self.SUT_PATCH + ".CommitMessageHookRunner")
        # Default return code SUCCESS
        self.mock_hook_runner.return_value.run.return_value = ExitCode.SUCCESS
        self.mock_sys = self.create_patch(self.SUT_PATCH + ".sys")
        self.mock_os = self.create_patch(self.SUT_PATCH + ".os")

        # When a YAML config implementation is constructed, return our mock
        self.mock_yaml_config = MagicMock(spec=CommitHookConfig)
        self.create_patch(
            self.SUT_PATCH + ".CommitHookConfigYAMLImpl"
        ).return_value = self.mock_yaml_config

        # When a default config implementation is constructed, return our mock
        self.mock_default_config = MagicMock(spec=CommitHookConfig)
        self.create_patch(
            self.SUT_PATCH + ".CommitHookConfigDefaultImpl"
        ).return_value = self.mock_default_config

        self.mock_logging = self.create_patch(self.SUT_PATCH + ".logging")

        self.create_patch('builtins.open')

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

    def test_get_config_with_yaml_config_file(self):
        self.mock_os.path.isfile.return_value = True
        self.assertEqual(
            sut.get_config(),
            self.mock_yaml_config,
            "A YAML implementation was not returned")

    def test_get_config_without_yaml_config_file(self):
        self.mock_os.path.isfile.return_value = False

        self.assertEqual(
            sut.get_config(),
            self.mock_default_config,
            "A default implementation was not returned")

        self.assertEqual(
            1,
            len(self.mock_logging.method_calls),
            "A warning should get logged to the console")
