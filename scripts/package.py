"""
    Generate OS specific executable
"""
import os
import platform
import sys
from shutil import copy2 as copy
from stat import ST_MODE

import PyInstaller.__main__

if __name__ == "__main__":
    OS_PREFIX: str = platform.system().lower()

    if OS_PREFIX == "darwin":
        OS_PREFIX = "mac"

    EXE_NAME: str = "commit-msg"
    EXE_FILE_FOLDER = os.path.join('dist', OS_PREFIX)

    # Hidden import mends PyInstaller moduleNotFound errors
    PyInstaller.__main__.run([
        "--onefile",
        "--hidden-import=_cffi_backend",
        "--distpath=%s" % EXE_FILE_FOLDER,
        "--name=%s" % EXE_NAME,
        os.path.join("src", "main", "commit_msg_hook.py"),
    ])

    # Remove file extension from executable
    if OS_PREFIX == "windows":
        FINAL_EXE_PATH = os.path.join(EXE_FILE_FOLDER, EXE_NAME)
        os.replace(FINAL_EXE_PATH + ".exe", FINAL_EXE_PATH)

    # add executable permission for Unix systems
    if OS_PREFIX != "windows":
        FINAL_EXE_PATH = os.path.join(EXE_FILE_FOLDER, EXE_NAME)
        print(FINAL_EXE_PATH)
        print(oct(os.stat(FINAL_EXE_PATH)[ST_MODE]))
        os.chmod(FINAL_EXE_PATH, 0o744)
        print(oct(os.stat(FINAL_EXE_PATH)[ST_MODE]))

    # As a work around, we must trick python to make this import happen
    # otherwise, we'll get:
    #   ValueError: attempted relative import beyond top-level package
    sys.path.append(".")
    from src.main.config.commit_hook_config_yaml_impl import CommitHookConfigYAMLImpl

    CONFIG_FILE_NAME = CommitHookConfigYAMLImpl.CONFIG_FILE_NAME

    # Save config with executable
    copy(os.path.join("src", "main", CONFIG_FILE_NAME),
         os.path.join(EXE_FILE_FOLDER, CONFIG_FILE_NAME))
