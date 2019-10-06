import unittest
from unittest.mock import patch


class BaseUnitTest:
    """
        By wrapping BaseTestCase in this class, the test runner will not attempt to run it
    """

    class BaseTestCase(unittest.TestCase):
        """
            We will need this mocking in most, if not all, of our unit tests
        """

        def create_patch(self, name: str):
            patcher = patch(name)
            mock_value = patcher.start()
            self.addCleanup(patcher.stop)
            return mock_value
