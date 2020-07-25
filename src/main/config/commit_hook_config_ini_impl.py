"""
    Load configuration from INI file
"""

import logging
from configparser import ConfigParser

from src.main.config.commit_hook_config import CommitHookConfig


class CommitHookConfigINIImpl(CommitHookConfig):
    """
        Pull configuration from INI file object passed to constructor
    """
    CONFIG_FILE_NAME: str = "commit-msg-config.ini"

    class INIKeys:
        """
            Group INI settings together
        """
        ISSUE_PATTERN_CONFIG: str = "issue_pattern"
        ISSUE_URL_PREFIX: str = "issue_url_prefix"
        NO_ISSUE_PHRASE: str = "no_issue_phrase"
        PROTECTED_BRANCH_PREFIXES: str = "protected_branch_prefixes"

    class Sections:
        """
            Group INI section titles together
        """
        DEFAULT: str = "SETTINGS"

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
            try:
                parser = ConfigParser()
                parser.read_file(config_file)
                config_dict = parser[self.Sections.DEFAULT]
                self.__issue_pattern = config_dict[self.INIKeys.ISSUE_PATTERN_CONFIG]
                self.__no_issue_phrase = config_dict[self.INIKeys.NO_ISSUE_PHRASE]
                self.__issue_url_prefix = config_dict[self.INIKeys.ISSUE_URL_PREFIX]
                self.__protected_branch_prefixes = \
                    [
                        branch.strip() for branch in
                        config_dict[self.INIKeys.PROTECTED_BRANCH_PREFIXES].split(",")
                    ]
            except Exception as error_thrown:
                logging.error("Check the format of: %s",
                              config_file.name if "name" in config_file else "unknown")
                raise error_thrown
        else:
            raise Exception("No configuration file found")
        config_file.close()

    def get_issue_pattern(self) -> str:
        return self.__issue_pattern

    def get_no_issue_phrase(self) -> str:
        return self.__no_issue_phrase

    def get_protected_branch_prefixes(self) -> list:
        return self.__protected_branch_prefixes

    def get_issue_url_prefix(self) -> str:
        return self.__issue_url_prefix
