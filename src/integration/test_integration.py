import os
import shutil
import stat
import time
import unittest


def enable_777_for_user_and_other(path):
    os.chmod(path, stat.S_IRWXO | stat.S_IRWXU)


def recursive_make_files_writable(path):
    for root, dirs, files in os.walk(path):
        for _dir in dirs:
            enable_777_for_user_and_other(os.path.join(root, _dir))
        for file in files:
            enable_777_for_user_and_other(os.path.join(root, file))


class TestIntegration(unittest.TestCase):
    test_repo_path: str
    abs_dist_path: str

    def setUp(self):
        # Dist should only have one other folder in it - grab that one
        self.abs_dist_path = os.path.join('dist', os.listdir('dist')[0])

        # Convert relative path to absolute
        self.abs_dist_path = os.path.abspath(self.abs_dist_path)

        # Remove any existing files in test repo and make empty folder
        self.test_repo_path = "test_repo"
        if os.path.isdir(self.test_repo_path):
            recursive_make_files_writable(os.path.abspath(self.test_repo_path))
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
            shutil.copy2(
                os.path.join(self.abs_dist_path, file_to_copy),
                os.path.join(hooks_folder, file_to_copy))

        # Tell git to use our hook
        os.system("git config core.hooksPath " + os.path.abspath(hooks_folder))

        # Make hook executable
        os.chmod(os.path.join(hooks_folder, "commit-msg"), stat.S_IRWXU | stat.S_IRWXO)

    def test_commit_message_is_edited(self):
        file_to_commit_path = "example.txt"
        with open(file_to_commit_path, 'w') as file_to_commit:
            file_to_commit.write("content here")

        # stage file
        os.system("git add " + file_to_commit_path)

        # commit file
        commit_message = "added example file"
        os.system('git config user.name pytest')
        os.system('git config user.email pytest@integration.com')

        os.system('git checkout -b feature/GH-123-awesome-new-thing')

        # Give git a moment to switch branches
        time.sleep(2)

        os.system('git commit -m "%s"' % commit_message)

        # Give the hook N seconds to run
        time.sleep(5)

        # Save commit message after hook should have run
        commit_message_after_hook: str = os.popen("git log -n 1 --format=\"%s\"").read()

        self.assertEqual(commit_message_after_hook.strip(), "GH-123: %s" % commit_message,
                         "Commit message was not edited correctly")
