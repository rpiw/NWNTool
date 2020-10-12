import unittest
from mainLib import NWN
import pathlib


class TestNWN(unittest.TestCase):
    def test_init(self):
        n = NWN(".", "enhanced_edition")
        self.assertEqual(n.version, "enhanced_edition")
        self.assertEqual(n.path, pathlib.Path(""))


if __name__ == '__main__':
    unittest.main()
