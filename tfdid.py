import argparse
import os
from utils.decorators import log


@log
def initialize():
    parser = argparse.ArgumentParser(
        prog="tfdid", description="A tool to display storage usage", epilog="Beep Boop"
    )
    parser.add_argument(
        "directory", metavar="D", default="~", action="store", help="directory to scan"
    )
    parser.add_argument(
        "-s",
        metavar="SIZE",
        action="store",
        default="block",
        choices=["K", "M", "G", "T", "P", "E"],
        help="scale block size by SIZE (default: %(default)s)",
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", default=False, help="start with GUI"
    )

    args = parser.parse_args()
    print(args)


def generate_directory_tree(dir_path):
    raise Exception("woops")
    paths = []
    for root, _, files in os.walk(dir_path):
        paths.append(root)
        paths.extend(os.path.join(root, _file) for _file in files)

    return paths


if __name__ == "__main__":
    initialize()
