from __future__ import print_function
import os
import hashlib
from typing import List
from termcolor import colored, cprint
import sys
from .custom_error import CustomError


def error_print(*args, **kwargs):
    """
    same as print but prints to stderr

    :param args:
    :param kwargs:
    :return:
    """
    print(*args, file=sys.stderr, **kwargs)


def color_print(*args, color: str = 'blue', **kwargs):
    """
    same as print but colored

    :param color:
    :param args:
    :param kwargs:
    :return:
    """
    args = [colored(str(x), color) for x in args]
    print(*args, **kwargs)


def are_files_equal(file_1: str, file_2: str, chunk_size: int = 1024) -> bool:
    """
    reads chunks of blocks for both files and checks them to be equal by comparing hashes

    :param chunk_size: size of chunk to be read
    :param file_1: path to file
    :param file_2: path to file
    :return: True, if files are equal, False otherwise
    """
    if not (os.path.isfile(file_1) and os.path.isfile(file_2)):
        raise CustomError("Paths are not dirs")
    try:
        if os.path.getsize(file_1) != os.path.getsize(file_2):
            return False
        hash_1 = hashlib.sha1()
        hash_2 = hashlib.sha1()
        with open(file_1, 'rb') as fd_1:
            with open(file_2, 'rb') as fd_2:
                while True:
                    data_1 = fd_1.read(chunk_size)
                    data_2 = fd_2.read(chunk_size)
                    hash_1.update(data_1)
                    hash_2.update(data_2)
                    if not data_1 or not data_2:
                        break
        return hash_1.hexdigest() == hash_2.hexdigest()
    except Exception:
        raise


def get_files_from_directory(path_to_directory: str) -> List[str]:
    """
    recursively walks target directory and returns all files which can be read

    :param path_to_directory: path to a valid directory
    :return: a list of absolute paths of files inside target directory
    """
    all_files = []
    for root, directories, files in os.walk(path_to_directory):
        all_files += [
            os.path.abspath(os.path.join(root, file_name)) for file_name in files if
            os.path.isfile(os.path.join(root, file_name)) and os.access(os.path.join(root, file_name), os.R_OK)
        ]
    return all_files


def get_local_path_of_files_from_directory(path_to_directory: str) -> List[str]:
    """
    same as above function but returns relative paths only

    :param path_to_directory: path to a valid directory
    :return: a list of relative paths of files inside target directory, relative towards directory
    """
    all_files = []
    for root, directories, files in os.walk(path_to_directory):
        all_files += [
            os.path.join(root, file_name)[len(path_to_directory):] for file_name in files if
            os.path.isfile(os.path.join(root, file_name)) and os.access(os.path.join(root, file_name), os.R_OK)
        ]
    return all_files


def are_folders_equal(folder_1: str, folder_2: str) -> bool:
    """

    :param folder_1: path to a directory
    :param folder_2: path to a directory
    :return: True, if folders are equal, false otherwise
    """
    if not (os.path.isdir(folder_1) and os.path.isdir(folder_2)):
        raise CustomError("Paths are not dirs")
    files_1 = get_files_from_directory(folder_1)
    files_2 = get_files_from_directory(folder_2)
    if len(files_1) != len(files_2):
        return False
    for i, j in zip(files_1, files_2):
        if not are_files_equal(i, j):
            return False
    return True

