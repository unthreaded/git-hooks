import unittest


class TestCommitHook(unittest.TestCase):

    def test_dummy_starter_1(self):
        self.assertTrue(True)

    def test_dummy_starter_2(self):
        self.assertFalse(False)

    def test_dummy_failing_test(self):
        self.assertFalse(True)


if __name__ == '__main__':
    unittest.main()
