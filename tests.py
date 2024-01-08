import unittest
import os
import io
import sys
import contextlib
from classes.parser import DirectoryScan


@contextlib.contextmanager
def captured_output():
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def validate_args(args, parser):
    with captured_output() as (out, err):
        try:
            parser.parse_args(args)
            return True
        except SystemExit as _:
            return False


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

    def test_fails_with_bad_args(self):
        self.assertFalse(validate_args(["-z"], self.dirscan.parser))
        self.assertTrue(validate_args(["-a"], self.dirscan.parser))

    def test_size_scale_failure(self):
        self.assertFalse(validate_args(["-s", "B"], self.dirscan.parser))
        self.assertTrue(validate_args(["-s", "K"], self.dirscan.parser))


if __name__ == "__main__":
    unittest.main()
