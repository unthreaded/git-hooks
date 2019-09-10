"""
    Baseline configuration interface
"""
from abc import ABC, abstractmethod


class CommitHookConfig(ABC):
    """
        Interface of sorts for our overall configuration
    """

    @abstractmethod
    def get_issue_pattern(self) -> str:
        """
            Intended to return the simplest regular expression for a ticket or issue number
        """

    @abstractmethod
    def get_no_issue_phrase(self) -> str:
        """
            For situations where work is done without an issue number,
            this is intended to be the default issue phrase
        """

    @abstractmethod
    def get_protected_branch_prefixes(self) -> list:
        """
            Returns zero or more branch prefixes that should NOT be touched
        """

    @abstractmethod
    def get_issue_url_prefix(self) -> str:
        """
            Returns the prefix to link to an issue
        """
