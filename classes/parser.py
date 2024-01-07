import argparse
import os
from pathlib import Path
from utils.decorators import log


class DirectoryScan:
    def __init__(self) -> None:
        # TODO: store results in a Trie
        self.scan_results = {}
        self.parser = self.__init_parser()
        self.__parse_args(self.parser.parse_args())
        self.size_scale = ["K", "M", "G", "T", "P", "E"]
        # directory tree components
        self.dir_space = "    "
        self.dir_branch = "│   "
        self.dir_item = "├── "
        self.dir_last = "└── "

    @log
    def __init_parser(self) -> argparse.ArgumentParser:
        # argparse self.parser requires a directory or uses the default 'dir_path'.
        parser = argparse.ArgumentParser(
            prog="tfdid",
            description="A tool to display storage usage",
            usage="tfdid [directory] [-h] [-i] [-a]",
            epilog="Beep Boop",
        )
        # The default directory is the current directory the user is in
        parser.add_argument(
            "directory",
            metavar="directory",
            nargs="?",
            default=f"{os.getcwd()}",
            action="store",
            help="directory to scan (default: current directory)",
        )
        # optionally search hidden files and folders
        # TODO: add 'a' as a sub-argument to another argument that sets the mode
        # TODO: make "tree"-like functionality with sizes as default mode
        # TODO: gui mode required for more detailed graph?
        parser.add_argument(
            "-a",
            "--all",
            action="store_true",
            default=False,
            help="search hidden files and folders",
        )
        """
        change the output scale for SIZE.
        Scaling default is in blocks, and is optionally scaled up in bytes using this option
        Ex: KB = blocks x 1024 / 512 (512 bytes in a block)
        """
        parser.add_argument(
            "-s",
            "--size",
            metavar="SIZE",
            action="store",
            default="block",
            choices=self.size_scale,
            help="scale block size by SIZE (default: %(default)s). Choices: %(choices)s",
        )

        # TODO: enable GUI
        parser.add_argument(
            "-i",
            "--interactive",
            action="store_true",
            default=False,
            help="start with GUI",
        )

        return parser

    def __parse_args(self, args: argparse.Namespace):
        print("ARGS :", args)

        # check if target directory exists
        if not Path(args.directory).exists():
            self.parser.error("directory does not exist")

        # validate size arg
        if args.size not in self.size_scale:
            self.parser.error(f"{self.size_scale} is not a valid size. ")

        # TODO: check args and throw error
