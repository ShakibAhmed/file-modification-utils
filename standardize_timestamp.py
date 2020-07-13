"""
I have some images with filenames that may have a timestamp, but the timestamp may have a different format or some extra
text. I want to convert these to the following format: YYYYmmdd_HHMMSS, so that I can sort by filename and navigate the
files more easily.

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


def standardize_timestamp(root_directory):
    full_dir_contents = listdir(root_directory)
    list_of_files = []
    for content in full_dir_contents:
        if isfile(join(root_directory, content)):
            list_of_files.append(content)

    for file in list_of_files:
        filename = str(file.split('.')[0])
        extension = str(file.split('.')[1])

        # Regex 1: Don't select filenames that are already in a standardized timestamp
        # Regex 2: Find filenames that have non-digits
        if not re.search("[\\d]+_[\\d]+", filename) and re.search("[\\D]", filename):
            if extension == "mp4": # For mp4s, a millisecond is recorded as well
                removed_non_digits = re.sub('\\D', '', file)[:-1]
            else:
                removed_non_digits = re.sub('\\D', '', file)

            if len(removed_non_digits) == 14:
                old_filename_dt = datetime.strptime(removed_non_digits, "%Y%m%d%H%M%S")
                new_filename = datetime.strftime(old_filename_dt, "%Y%m%d_%H%M%S") + "." + extension

                print(f"File {file} (Non-standard time) is being renamed to {new_filename}.")

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
        standardize_timestamp(sys.argv[1])
    except IndexError:
        print("Please enter the directory!")
