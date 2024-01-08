import argparse
from pathlib import Path
from utils.decorators import log


class DirectoryScan:
    def __init__(self) -> None:
        # TODO: store results in a Trie
        self.scan_results = {}
        self.size_scale = None
        self.directory = Path.cwd()
        self.search_all = False
        self.parser = self._init_parser()
        self._parse_args(self.parser.parse_args())
        self.file_tree = []
        # directory tree components
        self.dir_space = "    "
        self.dir_branch = "│   "
        self.dir_item = "├── "
        self.dir_last = "└── "

    @log
    def _init_parser(self) -> argparse.ArgumentParser:
        # argparse self.parser requires a directory or uses the default 'dir_path'.
        parser = argparse.ArgumentParser(
            prog="tfdid",
            description="A tool to display storage usage",
            usage="tfdid [directory] [-h] [options]",
            epilog="",
        )
        # The default directory is the current directory the user is in
        parser.add_argument(
            "directory",
            metavar="directory",
            nargs="?",
            default=f"{self.directory}",
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
            dest="all",
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
            dest="size",
            action="store",
            default="block",
            choices=["K", "M", "G", "T", "P", "E"],
            help="scale block size by SIZE (default: %(default)s). Choices: %(choices)s",
        )
        parser.add_argument(
            "-d",
            "--depth",
            dest="depth",
            action="store",
            default="4",
            help="only search this many directories deep (default: %(default)s)",
        )

        # TODO: enable GUI
        parser.add_argument(
            "-i",
            "--interactive",
            dest="interactive",
            action="store_true",
            default=False,
            help="start with GUI",
        )

        return parser

    def _parse_args(self, args: argparse.Namespace):
        # check if target directory exists
        if not Path(args.directory).exists():
            self.parser.error("directory does not exist")
        else:
            self.directory = args.directory

        self.size_scale = args.size
        self.search_all = args.all

        # TODO: check args and throw error

    def run_dir_scan(self, dir_path: Path = Path("."), prefix: str = ""):
        # TODO: add file / directory sizes
        if dir_path == Path("."):
            dir_path = Path(self.directory)
        dir_tree = list(dir_path.iterdir())
        structure = [self.dir_item] * (len(dir_tree) - 1) + [self.dir_last]

        for glyph, path in zip(structure, dir_tree):
            yield prefix + glyph + path.name
            if path.is_dir():
                extension = (
                    self.dir_branch if glyph == self.dir_item else self.dir_space
                )
                yield from self.run_dir_scan(path, prefix=prefix + extension)
