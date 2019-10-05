"""
    Generate OS specific executable
"""
import os
import platform

import PyInstaller.__main__

OS_PREFIX: str = platform.system().lower()

if OS_PREFIX == "darwin":
    OS_PREFIX = "mac"

EXE_NAME: str = "commit_msg"
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
FINAL_EXE_PATH = os.path.join(EXE_FILE_FOLDER, EXE_NAME)
os.rename(FINAL_EXE_PATH + ".exe", FINAL_EXE_PATH)
