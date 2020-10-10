import unittest
import scrapper
import exceptions


class TestScrapperWebsite(unittest.TestCase):

    def test_init(self):
        raise_them = ["", "https://blabla.com_", "ILoveYouToo", "google.com", "http://", "lody", "https://\n.com"]
        for www in raise_them:
            with self.assertRaises(exceptions.InvalidUrl):
                scrapper.Website(www)


if __name__ == '__main__':
    unittest.main()
