import unittest
from mainLib import NWN, Pair
import pathlib


class TestNWN(unittest.TestCase):
    def test_init(self):
        n = NWN(".", "enhanced_edition")
        self.assertEqual(n.version, "enhanced_edition")
        self.assertEqual(n.path, pathlib.Path(""))


class TestPair(unittest.TestCase):
    def test_init(self):
        p = Pair(1, 2)
        self.assertEqual(p.first, 1)
        self.assertEqual(p.second, 2)

    def test_setitem(self):
        p = Pair()
        p[0] = "bla"
        p[1] = False
        self.assertEqual(p.first, "bla")
        self.assertFalse(p[1])

        with self.assertRaises(TypeError):
            p.__setitem__(2.0, True)
        with self.assertRaises(IndexError):
            p.__setitem__(-1, None)

    def test_getitem(self):
        p = Pair(1, 2)
        self.assertEqual(p[0], 1)
        self.assertEqual(p[1], 2)

        with self.assertRaises(IndexError):
            p[2]


if __name__ == '__main__':
    unittest.main()
