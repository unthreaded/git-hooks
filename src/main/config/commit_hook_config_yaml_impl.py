"""
    Load configuration from INI file
"""

import yaml

from src.main.config.commit_hook_config import CommitHookConfig


class CommitHookConfigYAMLImpl(CommitHookConfig):
    """
        Pull configuration from INI file object passed to constructor
    """
    CONFIG_FILE_NAME: str = "commit-msg-config.yml"

    class YAMLKeys:
        """
            Group YAML settings together
        """
        ISSUE_PATTERN_CONFIG: str = "issue_pattern"
        ISSUE_URL_PREFIX: str = "issue_url_prefix"
        NO_ISSUE_PHRASE: str = "no_issue_phrase"
        PROTECTED_BRANCH_PREFIXES: str = "protected_branch_prefixes"

    __issue_pattern: str
    __no_issue_phrase: str
    __issue_url_prefix: str
    __protected_branch_prefixes: list

    def __init__(self, config_file) -> None:
        """
        Code creating this object is expected to catch any exceptions raised

        :param config_file:
            File object for ini file
        """
        if config_file:
            config_dict = yaml.safe_load(config_file)
            self.__issue_pattern = config_dict[self.YAMLKeys.ISSUE_PATTERN_CONFIG]
            self.__no_issue_phrase = config_dict[self.YAMLKeys.NO_ISSUE_PHRASE]
            self.__issue_url_prefix = config_dict[self.YAMLKeys.ISSUE_URL_PREFIX]
            self.__protected_branch_prefixes = \
                config_dict[self.YAMLKeys.PROTECTED_BRANCH_PREFIXES]

            config_file.close()
        else:
            raise Exception("File object cannot be none")
        super().__init__()

    def get_issue_pattern(self) -> str:
        return self.__issue_pattern

    def get_no_issue_phrase(self) -> str:
        return self.__no_issue_phrase

    def get_protected_branch_prefixes(self) -> list:
        return self.__protected_branch_prefixes

    def get_issue_url_prefix(self) -> str:
        return self.__issue_url_prefix
