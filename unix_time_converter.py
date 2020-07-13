"""
I have some images with filenames stored in Unix time. I want to convert these to the following format: YYYYmmdd_HHMMSS,
so that I can sort by filename and navigate the files more easily.

This script will loop through a given file directory. For each file:
1. Read the name of the file and determine if it's in epoch/Unix time.
2. Convert the time to YYYYmmdd_HHMMSS.
3. Rename the file.
"""
from datetime import datetime
from os import listdir, rename
from os.path import isfile, join
import re
import sys


def unix_time_converter(root_directory):
    full_dir_contents = listdir(root_directory)
    list_of_files = []
    for content in full_dir_contents:
        if isfile(join(root_directory, content)):
            list_of_files.append(content)

    for file in list_of_files:
        filename = str(file.split('.')[0])
        extension = str(file.split('.')[1])

        # Regex 1: Unix time, represented with 10 digits
        # Regex 2: If the filename has any non-digits, it's not in Unix time
        if re.search("[0-9]{10}", filename) and not re.search("[\\D]", filename):
            unix_ts = float(filename) / 1000
            converted_ts = datetime.fromtimestamp(unix_ts).strftime('%Y%m%d_%H%M%S')
            new_filename = converted_ts + "." + extension
            print(f"File {file} (Unix time) is being renamed to {new_filename}.")

            old_path = root_directory + '\\' + file
            new_path = root_directory + '\\' + new_filename
            try:
                rename(old_path, new_path)
            except FileExistsError:
                print(f"File {file} can't be renamed. The new filename {new_filename} already exists! This file may"
                      f"be a duplicate.")
                continue


if __name__ == "__main__":
    try:
        unix_time_converter(sys.argv[1])
    except IndexError:
        print("Please enter the directory!")
