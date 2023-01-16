"""
    Check codebase for lint violations
"""
import subprocess
import sys

DOCSTRING_REQUIREMENT = 'C0111'

TOO_FEW_PUBLIC_METHODS = 'R0903'


def lint(ignore_rules: list, directories: list):
    """
    :param ignore_rules: Pylint constants for rules
    :param directories: File paths to lint
    """
    print(f"Linting: {directories}", flush=True)

    ignore_string: str = ",".join(ignore_rules)

    exit_code = subprocess.run(['pylint',
                                f"--disable={ignore_string}"
                                ] + directories,
                               check=False).returncode
    if exit_code != 0:
        print("Lint violation found.")
        sys.exit(exit_code)


lint([TOO_FEW_PUBLIC_METHODS],
     [
         'src.main',
         'scripts'
     ])

lint([DOCSTRING_REQUIREMENT, TOO_FEW_PUBLIC_METHODS],
     ['src.test', 'src.integration'])
