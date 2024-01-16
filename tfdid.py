from classes.parser import DirectoryScan


if __name__ == "__main__":
    parser = DirectoryScan()
    for line in parser.run_dir_scan():
        print(line)
