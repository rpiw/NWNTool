import unittest
from main import NWN


class TestNWN(unittest.TestCase):
    def test_init(self):
        n = NWN("", "enhanced_edition")
        self.assertEqual(n.version, "enhanced_edition")
        self.assertEqual(n.path, "")


if __name__ == '__main__':
    unittest.main()
