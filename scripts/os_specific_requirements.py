"""
    Anything our build needs to do for a specific OS goes here
"""
import os
import platform

if __name__ == "__main__":
    OS_PREFIX: str = platform.system().lower()

    print("Running OS setup")
    print(f"OS: {OS_PREFIX}")

    if OS_PREFIX == "darwin":
        os.system("brew install upx")
