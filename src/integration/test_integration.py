import os
import shutil
import stat
import sys
import time
import unittest


class TestIntegration(unittest.TestCase):
    test_repo_path: str
    abs_dist_path: str

    def setUp(self):
        """
            When the pipeline builds the hook,
            the folder containing the binary will be passed as a command line argument
        """
        self.assertEqual(len(sys.argv), 3, "Not enough command line arguments")

        self.abs_dist_path = sys.argv[2]
        self.assertIsNotNone(self.abs_dist_path, "Did not receive executable path")

        # Convert relative path to absolute
        self.abs_dist_path = os.path.abspath(self.abs_dist_path)

        # Remove any existing files in test repo and make empty folder
        self.test_repo_path = "test_repo"
        if os.path.isdir(self.test_repo_path):
            shutil.rmtree(self.test_repo_path)
        self.assertFalse(os.path.isdir(self.test_repo_path), "Test repo wasn't removed")
        os.mkdir(self.test_repo_path)

        # Move into test repo
        os.chdir(self.test_repo_path)

        os.system("git init")

        # Make hooks folder and copy binary into folder
        hooks_folder = os.path.join(".git", "hooks")
        os.makedirs(hooks_folder, exist_ok=True)
        for file_to_copy in os.listdir(self.abs_dist_path):
            shutil.copy2(os.path.join(self.abs_dist_path, file_to_copy), os.path.join(hooks_folder, file_to_copy))

        # Tell git to use our hook
        os.system("git config core.hooksPath " + os.path.abspath(hooks_folder))

        # Make hook executable
        os.chmod(os.path.join(hooks_folder, "commit-msg"), stat.S_IEXEC)

    def test_commit_message_is_edited(self):
        file_to_commit_path = "example.txt"
        file_to_commit = open(file_to_commit_path, 'w')
        file_to_commit.write("content here")
        file_to_commit.close()

        # stage file
        os.system("git add " + file_to_commit_path)

        # commit file
        commit_message = "added example file"
        os.system('git commit -m "%s"' % commit_message)

        # Give the hook N seconds to run
        time.sleep(5)

        # Save commit message after hook should have run
        commit_message_after_hook: str = os.popen("git log -n 1 --format=\"%s\"").read()

        self.assertEqual(commit_message_after_hook.strip(), "NOGH: %s" % commit_message,
                         "Commit message was not edited correctly")
