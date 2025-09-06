"""
    Shared code betweens scripts
"""
import platform

__os_alias_temp: str = platform.system().lower()

OS_ALIAS: str = "mac" if __os_alias_temp == "darwin" else __os_alias_temp
EXE_FILE_FOLDER = 'dist'
