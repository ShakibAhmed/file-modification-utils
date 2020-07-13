from datetime import datetime
from os import listdir, utime, scandir
from os.path import isfile, join
import sys
import time
# from PIL import Image, ExifTags

from pathlib import Path
import exifread
# from exif import Image

from PIL import Image
from PIL.ExifTags import TAGS
import pandas as pd


def read_properties(root_directory):
    image_data_list = []
    current_dir = Path(root_directory)
    for path in current_dir.iterdir():
        # Datetime read directly from the file
        properties_modified_time = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y%m%d_%H%M%S")
        exif_datetime = None
        exif_datetime_original = None
        exif_datetime_digitized = None

        # Generate datetime from the filename
        filename = str(path.name.split('.')[0])
        date_from_filename = str(filename.split('-')[1])
        year = int(date_from_filename[0:4])
        month = int(date_from_filename[4:6])
        day = int(date_from_filename[6:8])

        modified_time_from_filename = datetime(year=year, month=month, day=day, hour=0, minute=0, second=0)
        modified_time_from_filename = modified_time_from_filename.strftime("%Y%m%d_%H%M%S")

        # Read EXIF data
        with open(str(path), 'rb') as image_file:
            image = Image.open(image_file)
            exif_data = image.getexif()
            for exif_tag, value in exif_data.items():
                decoded_exif_tag = TAGS.get(exif_tag, exif_tag)
                if decoded_exif_tag == "DateTime":
                    exif_datetime = value
                if decoded_exif_tag == "DateTimeOriginal":
                    exif_datetime_original = value
                if decoded_exif_tag == "DateTimeDigitized":
                    exif_datetime_digitized = value
            image_file.close()

        try:
            modified_time_from_exif_datetime = datetime.strptime(exif_datetime, "%Y:%m:%d %H:%M:%S").strftime("%Y%m%d_%H%M%S")
            modified_time_from_exif_datetime_original = datetime.strptime(exif_datetime_original, "%Y:%m:%d %H:%M:%S").strftime("%Y%m%d_%H%M%S")
            modified_time_from_exif_datetime_digitized = datetime.strptime(exif_datetime_digitized, "%Y:%m:%d %H:%M:%S").strftime("%Y%m%d_%H%M%S")
        except TypeError:
            modified_time_from_exif_datetime = None
            modified_time_from_exif_datetime_original = None
            modified_time_from_exif_datetime_digitized = None


            # print("The file {} does not have the correct modified date. New modified time: {} "
            #      .format(path.name, modified_time_file))

        single_image_data = {
            # File attributes
            "filename": filename,
            "extension": path.name.split('.')[1],
            # Datetime read from the file
            "properties_modified_time": properties_modified_time,
            "exif_datetime": exif_datetime,
            "exif_datetime_original": exif_datetime_original,
            "exif_datetime_digitized": exif_datetime_digitized,
            # Generated datetime
            "modified_time_from_filename": modified_time_from_filename,
            "modified_time_from_exif_datetime": modified_time_from_exif_datetime,
            "modified_time_from_exif_datetime_original": modified_time_from_exif_datetime_original,
            "modified_time_from_exif_datetime_digitized": modified_time_from_exif_datetime_digitized
        }
        image_data_list.append(single_image_data)

    image_data_df = pd.DataFrame(data=image_data_list)
    # image_data_df.to_csv("all_image_data.csv") # TODO: commenting cuzdon't want to accidentally overwrite the file

    # if (year == 2019 and month >= 11) or year == 2020:
    #     print(f"The file {filename} has a correct modified date and will not be updated.")
    #     continue


    #     new_modified_date_unix = time.mktime(new_modified_date.timetuple())
    #     print(f"The file {filename} will have a new modified time of {new_modified_date}.")
    #     # utime(file_location, (new_modified_date_unix, new_modified_date_unix))
    #

# Using ExifRead
# tags = exifread.process_file(image_file, stop_tag="EXIF DateTimeOriginal", details=False)
# for key, value in tags.items():
#     if key == "EXIF DateTimeOriginal":
#         modified_time_exif = value

if __name__ == "__main__":
    try:
        read_properties(sys.argv[1])
    except IndexError:
        print("Please enter the directory!")
