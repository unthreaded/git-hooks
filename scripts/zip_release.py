"""
    Zip executable for release
"""
from shutil import make_archive

from helpers import OS_ALIAS, EXE_FILE_FOLDER

if __name__ == "__main__":
    # Output a zip file with the configuration file + executable
    # in the current working directory
    zip_file_name = OS_ALIAS.capitalize()
    make_archive(zip_file_name, 'zip', EXE_FILE_FOLDER)
    print(f"Wrote zip file: {zip_file_name}")
