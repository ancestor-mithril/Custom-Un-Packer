import re
from typing import List, Tuple, BinaryIO
import os

from utils import get_files_from_directory, CustomError
from utils.utils import get_local_path_of_files_from_directory


def get_metadata_from_archive(target_archive: str, chunk_size: int = 1024) -> bin:
    """
    reads binary from file until it finds the binary string which signify metadata closing tag
    returns metadata binary and raises errors if metadata closing tag was not found

    :param target_archive: the path to an already created archive
    :param chunk_size: the size of chunk to be read from archive
    :return: the metadata string at the beginning of archive in binary
    """
    metadata_end = b"</?METADATA>"
    with open(target_archive, "rb") as fp:
        x = fp.read(chunk_size)
        end_index = x.find(metadata_end)
        while end_index == -1:
            y = fp.read(chunk_size)
            x += y
            end_index = x.find(metadata_end)
            if not y:
                if end_index == -1:
                    raise CustomError("Archive was corrupted")
                break

    return x[:end_index + len(metadata_end)]


def process_metadata(metadata: str) -> List[Tuple[str, str]]:
    """
    applies the expected regex on metadata and retrieves number of files in archive along with their names and size

    :param metadata: the metadata string at the beginning of archive
    :return: a list of tuples of files in archive and their space
    """
    metadata_pattern = re.compile(r"<\?METADATA>"
                                  r"<\?NO_FILES>(.*?)<\/\?NO_FILES>"
                                  r"(.*?)"
                                  r"<\/\?FILES>"
                                  r"<\/\?METADATA>")
    file_pattern = re.compile(r"<\?FILE><\?NAME>(.*?)<\/\?NAME><\?SIZE>(.*?)<\/\?SIZE><\/\?FILE>")
    data = re.match(metadata_pattern, metadata)
    if len(data.groups()) != 2:
        raise CustomError("Archive was corrupted")
    try:
        files_in_archive = int(data.group(1))
    except TypeError:
        raise CustomError("Archive was corrupted")
    files = re.findall(file_pattern, data.group(2))
    if len(files) != files_in_archive:
        raise CustomError("Archive was corrupted")
    return files


def get_archive_content(target_archive: str) -> Tuple[int, List[Tuple[str, str]]]:
    """

    :param target_archive: the path to an already created archive
    :return: metadata length and a list containing all files in archive along with their size
    """
    metadata = get_metadata_from_archive(target_archive)
    files = process_metadata(metadata.decode('utf-8', 'ignore'))
    return len(metadata), files


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


def unpack_file(file: str, size: int, fp: BinaryIO, chunk_size: int = 1024):
    """

    :param file:
    :param size:
    :param fp:
    :param chunk_size:
    :return: void
    """