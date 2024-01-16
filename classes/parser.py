import argparse
from collections.abc import Generator
from pathlib import Path
from utils.decorators import log


class DirectoryScan:
    def __init__(self) -> None:
        self.size_scale = "block"
        self.directory = Path.cwd()
        self.search_all = False
        self.parser = self._init_parser()
        self._parse_args(self.parser.parse_args())
        # directory tree glyphs
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
        parser.add_argument(
            "-a",
            "--all",
            dest="all",
            action="store_true",
            default=False,
            help="search hidden files and folders",
        )

        # change size scale from blocks to more human-readable formats
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

        return parser

    def _parse_args(self, args: argparse.Namespace) -> None:
        # check if target directory exists
        if not Path(args.directory).exists():
            self.parser.error("directory does not exist")
        else:
            self.directory = args.directory

        self.size_scale = args.size
        self.search_all = args.all

    def _convert_block_size(self, blocks: int) -> float:
        """
        change the output scale for SIZE.
        Scaling default is in blocks, and is optionally scaled up in bytes using this option
        Ex: KB = blocks / 1024
        """
        sizes = {"K": 1, "M": 2, "G": 3, "T": 4, "P": 5, "E": 6}
        if self.size_scale == "block":
            return blocks

        return round(blocks / (1024 ** sizes[self.size_scale]), 2)

    def run_dir_scan(
        self, dir_path: Path = Path("."), prefix: str = ""
    ) -> Generator[str, str, None]:
        """
        a recursive generator, given a valid Path object, will yield a visual tree
        structure line by line, prefixed by glyphs to draw the structure.
        Heavily helped by https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python/59109706#59109706
        """
        # add a "." to indicate the starting directory in the tree, then set working dir
        if dir_path == Path("."):
            print(
                f"[{str(self._convert_block_size(dir_path.stat().st_size))}{self.size_scale}]",
                "\033[34m.\033[0m",
            )
            dir_path = Path(self.directory)

        # search all folders if flag is used, otherwise skip over hidden folders prefixed with '.'
        if self.search_all:
            dir_tree = list(dir_path.iterdir())
        else:
            dir_tree = [
                d for d in dir_path.iterdir() if not str(d.name).startswith(".")
            ]

        # each item in the tree list is prefixed with a glyph and file/dir size
        structure = [self.dir_item] * (len(dir_tree) - 1) + [self.dir_last]

        for glyph, path in zip(structure, dir_tree):
            """
            yield current directory or file to the calling function to print
            print directories in blue
            """
            reset_color = "\033[0m"
            dir_color = "\033[34m" if path.is_dir() else reset_color

            yield f"{prefix}{glyph}[{str(self._convert_block_size(path.stat().st_size))}{self.size_scale}] {dir_color}{path.name}{reset_color}"

            # extends the prefix and recurses into directory if current path is a directory
            # appends dir_branch glyph if appropriate, otherwise spacing
            if path.is_dir():
                extension = (
                    self.dir_branch if glyph == self.dir_item else self.dir_space
                )
                # recursively yield from run_dir_scan generator
                yield from self.run_dir_scan(path, prefix=prefix + extension)
