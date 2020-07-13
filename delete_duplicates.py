import sys
import os
from pathlib import Path
import re
from time import gmtime, strftime
import logging
now = strftime("%Y%m%d_%H%M%S", gmtime())
logger = logging.getLogger('delete_duplicates')
hdlr = logging.FileHandler('logs/delete_duplicates/delete_duplicates_{}.log'.format(now))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


def delete_duplicates(root_directory):
    current_dir = Path(root_directory)
    for path in current_dir.iterdir():
        filename = str(path.name)
        if re.search(".*\(\d\).*", filename):
            logger.info("Deleting duplicate file {}!".format(filename))
            os.remove(str(path))


if __name__ == "__main__":
    try:
        # delete_duplicates(sys.argv[1])
        delete_duplicates(r"C:\Users\Shakib\Google Drive\Google Photos\2015\05")
    except IndexError:
        print("Please enter the directory!")