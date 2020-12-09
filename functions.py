"""Run the script as follows:
python a_seven.py --help
                => prints help
python a_seven.py -create_archive target_archive target_objects
    * where `target_objects` must be at least 1 directory or file in SSV format (space separated values)
                => fails if `target_archive` already exists or any `target_objects` does not
                => archives all content of `target_objects` to the `target_archive`
python a_seven.py -list_content target_archive
                => lists content of `target_archive` should it exist
python a_seven.py -full_unpack target_archive target_folder
                => fails if `target_folder` exists or `target_archive` does not
                => unpacks all content of `target_archive` into `target_folder`
python a_seven.py -unpack target_archive target_folder target_files
    * where `target_files` must be at least one or more files packed into `target_archive`
                => fails if `target_folder` exists or `target_archive` does not
                => fails if any of `target_files` is not inside `target_archive`
                => unpacks each one of `target_files` from `target_archive` into `target_folder`
"""
from typing import List

from utils import color_print


def run_help():
    """
    prints script documentation
    then exits program

    :return: void
    """
    color_print(__doc__)
    exit(0)


def run_create_archive(target_archive: str, *target_objects: List[str]):
    """
    adds each target_object to archive, if target_object is file, otherwise adds all content of target_object to archive
    and creates said archive
    then exits program

    :param target_archive: the path of the archive to be created; should be valid and not already exist
    :param target_objects: a list of paths to valid files or folders; should not be empty
    :return: void
    """
    exit(0)


def run_list_content(target_archive: str):
    """
    prints a list of files inside target_archive
    then exits program

    :param target_archive: the path to an already created archive
    :return: void
    """
    exit(0)


def run_full_unpack(target_archive: str, target_folder: str):
    """
    creates target_folder where it unpacks all content of target_archive
    then exits program

    :param target_archive: the path to an already created archive
    :param target_folder: the path to the unpack location directory; should not already exist
    :return: void
    """
    exit(0)


def run_unpack(target_archive: str, target_folder: str, *target_files: List[str]):
    """
    creates target_folder where it unpacks listed target_files from target_archive
    then exits program

    :param target_archive: the path to an already created archive
    :param target_folder: the path to the unpack location directory; should not already exist
    :param target_files: a list of files inside target_archive
    :return: void
    """
    exit(0)
