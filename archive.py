from io import BufferedWriter
from typing import List, Tuple, BinaryIO
import os

from utils import get_files_from_directory, CustomError
from utils.utils import get_local_path_of_files_from_directory


def get_archive_content(target_archive: str) -> List[str]:
    """

    :param target_archive: the path to an already created archive
    :return: a list containing all files in archive
    """
    return []


def get_input_files_for_archive(*target_objects: str) -> List[Tuple[str, str]]:
    """

    :param target_objects: a list of paths to valid files or folders; should not be empty
    :return: a list of tuples, of absolute paths of all target files or files inside target directories and their
             respective relative position that they should have inside archive
    """
    assert len(target_objects) > 0, "The list of files or directories ought to not be empty"
    return_list = []
    for obj in target_objects:
        if os.path.isdir(obj):
            return_list += zip(get_files_from_directory(obj), get_local_path_of_files_from_directory(obj))
        elif os.path.isfile(obj) and os.access(obj, os.R_OK):
            return_list.append((os.path.abspath(obj), os.path.basename(obj)))
        else:
            raise CustomError("Given paths are not valid")
    return return_list


def append_file_to_archive(file: str, fp: BinaryIO, chunk_size: int = 1024):
    """

    :param file: absolute path to the file to be written to archive
    :param fp: file pointer of archive
    :param chunk_size: the size of chunk to be read and written from file to archive
    :return: void
    """
    with open(file, "rb") as fp2:
        while True:
            data = fp2.read(chunk_size)
            if not data:
                break
            fp.write(data)

