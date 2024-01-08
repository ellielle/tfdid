from argparse import ArgumentError
import unittest
import os
from classes.parser import DirectoryScan


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.dirscan = DirectoryScan()

    def test_initializes_without_args(self):
        args = self.dirscan.parser.parse_args()
        self.assertEqual(args.directory, os.getcwd())
        self.assertFalse(args.all)
        self.assertFalse(args.interactive)
        self.assertEqual(args.size, "block")

    def test_initializes_with_args(self):
        args = self.dirscan.parser.parse_args(["~/", "-a", "-i"])
        self.assertEqual(args.directory, "~/")
        self.assertTrue(args.interactive)
        self.assertTrue(args.all)

    def test_initializes_with_size_scale(self):
        args = self.dirscan.parser.parse_args(["-s", "K"])
        self.assertEqual(args.size, "K")


"""
    def test_fails_with_nonexistent_directory(self):
        with self.assertRaises(Exception):
            self.dirscan.parser.parse_args(["d"])



    def test_size_scale_failure(self):
        with self.assertRaises(ArgumentError) as err:
            args = self.dirscan.parser.parse_args(["-s", "B"])

        self.assertTrue("invalid choice" in str(err.exception))
"""


if __name__ == "__main__":
    unittest.main()
