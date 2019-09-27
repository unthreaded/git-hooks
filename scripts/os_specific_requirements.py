import os
import platform

OS_PREFIX: str = platform.system().lower()

print("Running OS setup")
print("OS: %s" % OS_PREFIX)

if OS_PREFIX == "darwin":
    os.system("brew install libgit2")
