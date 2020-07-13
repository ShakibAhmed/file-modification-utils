import numpy as np
import pandas as pd
import sys
from datetime import datetime
from time import gmtime, mktime, strftime
from os import utime

import logging
now = strftime("%Y%m%d_%H%M%S", gmtime())
logger = logging.getLogger('update_modified_time')
hdlr = logging.FileHandler('logs/update_modified_time/update_modified_time_{}.log'.format(now))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


def read_file_data(root_directory):
    image_data_df = pd.read_csv('image_data.csv')
    cleaned_data = image_data_df[['filename', 'extension', 'modified_time_from_filename', 'modified_time_from_exif_datetime_original']]
    cleaned_data = cleaned_data[0:36965]

    for file_row in cleaned_data.itertuples():
        file_path = root_directory + "\\" + file_row.filename + "." + file_row.extension
        filename_date = datetime.strptime(file_row.modified_time_from_filename, "%Y%m%d_%H%M%S")

        if type(file_row.modified_time_from_exif_datetime_original) == str:
            # Checking if EXIF time matches the filename (sometimes it's before the date, in that case we don't use it)
            exif_date = datetime.strptime(file_row.modified_time_from_exif_datetime_original, "%Y%m%d_%H%M%S")
            if exif_date < filename_date:
                logger.info("EXIF datetime ({}) is before the filename datetime ({}) for file {}. EXIF time will not be"
                            " used!".format(exif_date, filename_date, file_row.filename))
                update_modified_time(filename_date, file_path)
            else:
                logger.info("EXIF datetime found for file {}. Using the following time: {}"
                            .format(file_row.filename, file_row.modified_time_from_exif_datetime_original))
                update_modified_time(exif_date, file_path)

        else:
            logger.info("No EXIF datetime found for file {}. Using the following time derived from the filename: {}"
                        .format(file_row.filename, file_row.modified_time_from_filename))
            update_modified_time(filename_date, file_path)


def update_modified_time(new_time, file_path):
    new_modified_date_unix = mktime(new_time.timetuple())
    utime(file_path, (new_modified_date_unix, new_modified_date_unix))
    logger.info("Updated the file at path {} to the following time: {}".format(file_path, new_time))


if __name__ == "__main__":
    try:
        read_file_data(sys.argv[1])
    except IndexError:
        print("Please enter the directory!")
