import os
from classes.parser import DirectoryScan


def generate_directory_tree(dir_path):
    raise Exception("woops")
    paths = []
    for root, _, files in os.walk(dir_path):
        paths.append(root)
        paths.extend(os.path.join(root, _file) for _file in files)

    return paths


if __name__ == "__main__":
    parser = DirectoryScan()
