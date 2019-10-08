"""
    Default configuration
"""
from src.main.config.commit_hook_config import CommitHookConfig


class CommitHookConfigDefaultImpl(CommitHookConfig):
    """
        Default values for all configuration items
    """

    def get_issue_url_prefix(self) -> str:
        return "https://github.com/unthreaded/git-hooks/issues/"

    def get_issue_pattern(self) -> str:
        return "GH-[0-9]+"

    def get_no_issue_phrase(self) -> str:
        return "NOGH"

    def get_protected_branch_prefixes(self) -> list:
        return ["dev", "release", "hotfix"]
