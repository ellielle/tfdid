# tfdid

tfdid (TF Did I Download?) is a cli tool written in Python to parse directory trees and display size information, similar to the `tree` utility, though not as fully-featured.

Why? I wanted to play around with recursive generators, mostly. And I wanted to look around at what bloats my WSL images so heavily over time.

## Features

- Displays directory structure with directory/file sizes
- Size is by default in blocks, can be scaled with `--size` to KB, MB, etc
- Omits hidden directories by default, enabled with `--all`

## Potential improvements

- [ ] Add option to only return X largest files or directories
- [ ] Add option to search for known file bloat, such as `node_modules`

## Requirements

- python 3.10+

## Instructions

- Clone repo `$ git clone git@github.com:ellielle/tfdid.git`
- Run tests with `$ python3 tests.py`
- Run with `$ python3 tfdid.py -h` for available options
