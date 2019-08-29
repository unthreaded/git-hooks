import unittest


class TestCommitHook(unittest.TestCase):

    def test_dummy_starter_1(self):
        self.assertTrue((2 - 1) == 1)

    def test_dummy_starter_2(self):
        self.assertFalse(1 == 2)


if __name__ == '__main__':
    unittest.main()
