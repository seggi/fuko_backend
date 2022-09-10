import os
import errno


def create_path(directory):
    try:
        os.makedirs(directory)
        return 200
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
