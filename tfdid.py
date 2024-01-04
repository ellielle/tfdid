import argparse
import os
from utils.decorators import log


@log
def initialize():
    # The default directory is the current directory the user is in
    dir_path = os.path.dirname(os.path.abspath(__file__))

    # argparse parser accepts directory, size and interactive arguments
    parser = argparse.ArgumentParser(
        prog="tfdid",
        description="A tool to display storage usage",
        usage="tfdid [directory] [options]",
        epilog="Beep Boop",
    )
    parser.add_argument(
        "directory",
        metavar="directory",
        default=f"{dir_path}",
        action="store",
        help="directory to scan (default: current directory)",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        default=False,
        help="search hidden files and folders",
    )
    parser.add_argument(
        "-s",
        "--size",
        metavar="size",
        action="store",
        default="block",
        choices=["K", "M", "G", "T", "P", "E"],
        help="scale block size by SIZE (default: %(default)s). Choices: %(choices)s",
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true", default=False, help="start with GUI"
    )

    args = parser.parse_args()
    print("ARGS :", args)
    print(os.fspath(dir_path))
    # TODO better handling of improper usage
    parser.error("Error here if options are bad")


def generate_directory_tree(dir_path):
    raise Exception("woops")
    paths = []
    for root, _, files in os.walk(dir_path):
        paths.append(root)
        paths.extend(os.path.join(root, _file) for _file in files)

    return paths


if __name__ == "__main__":
    initialize()
