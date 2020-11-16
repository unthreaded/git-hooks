"""
    Generate OS specific executable
"""
import os
import platform
import shutil
import sys
from shutil import copy2 as copy, rmtree

import PyInstaller.__main__

if __name__ == "__main__":
    # Clean up from previous build
    rmtree('dist', ignore_errors=True)
    rmtree('build', ignore_errors=True)

    OS_ALIAS: str = platform.system().lower()

    if OS_ALIAS == "darwin":
        OS_ALIAS = "mac"

    EXE_NAME: str = "commit-msg"
    EXE_FILE_FOLDER = os.path.join('dist', OS_ALIAS)

    # Hidden import mends PyInstaller moduleNotFound errors
    PyInstaller.__main__.run([
        "--onefile",
        "--hidden-import=_cffi_backend",
        "--distpath=%s" % EXE_FILE_FOLDER,
        "--name=%s" % EXE_NAME,
        os.path.join("src", "main", "commit_msg_hook.py"),
    ])

    # Remove file extension from executable
    if OS_ALIAS == "windows":
        FINAL_EXE_PATH = os.path.join(EXE_FILE_FOLDER, EXE_NAME)
        os.replace(FINAL_EXE_PATH + ".exe", FINAL_EXE_PATH)

    # As a work around, we must trick python to make this import happen
    # otherwise, we'll get:
    #   ValueError: attempted relative import beyond top-level package
    sys.path.append(".")
    from src.main.config.commit_hook_config_ini_impl import CommitHookConfigINIImpl

    CONFIG_FILE_NAME = CommitHookConfigINIImpl.CONFIG_FILE_NAME

    # Save config with executable
    copy(os.path.join("src", "main", CONFIG_FILE_NAME),
         os.path.join(EXE_FILE_FOLDER, CONFIG_FILE_NAME))

    # Output a zip file with the configuration file + executable
    # in the current working directory
    zip_file_name = OS_ALIAS.capitalize()
    shutil.make_archive(zip_file_name, 'zip', EXE_FILE_FOLDER)
    print("Wrote zip file: %s" % zip_file_name)
