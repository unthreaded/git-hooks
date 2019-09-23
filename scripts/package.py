import os
import platform

import PyInstaller.__main__

OS_PREFIX: str = platform.system().lower()

if OS_PREFIX == "darwin":
    OS_PREFIX = "mac"

PyInstaller.__main__.run([
    "--onefile",
    "--name=%s" % "commit_msg_%s.exe" % OS_PREFIX,
    os.path.join("src", "main", "commit_msg_hook.py"),
])
