import os
import errno


def create_path(directory):
    try:
        media_folder = os.path.normpath(directory)
        if not os.path.exists(media_folder):
            os.makedirs(media_folder)
            return 200
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
