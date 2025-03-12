import unittest
from genpage import *


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_good(self):
        md = "# wut"
        title = extract_title(md)
        self.assertEqual(title, "wut")

    def test_extract_titty_bad(self): 
        md = "## titty"
        with self.assertRaises(Exception):
            print(extract_title(md))