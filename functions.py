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
import errno
from typing import List
import os
from archive import get_archive_content, get_input_files_for_archive, append_file_to_archive, unpack_file, \
    prepare_archive_unpacking, empty_read_archive
from utils import color_print, CustomError


def run_help():
    """
    prints script documentation
    then exits program

    :return: void
    """
    color_print(__doc__)
    exit(0)


def run_create_archive(target_archive: str, *target_objects: str):
    """
    adds each target_object to archive, if target_object is file, otherwise adds all content of target_object to archive
    and creates said archive
    then exits program

    :param target_archive: the path of the archive to be created; should be valid and not already exist
    :param target_objects: a list of paths to valid files or folders; should not be empty
    :return: void
    """
    if os.path.exists(target_archive):
        raise CustomError("An archive with the same name already exists. Please select a new name for the archive")
    try:
        fp = open(target_archive, "wb")
    except OSError as e:
        raise CustomError(f"Error at creating target archive {e}")
    input_files = get_input_files_for_archive(*target_objects)
    for i in range(len(input_files) - 1):
        for j in range(i + 1, len(input_files)):
            if input_files[i][1] == input_files[j][1]:
                raise CustomError(
                    f"Files with duplicate name found after filtering:\n{input_files[i][0]}\n{input_files[j][0]}")

    archive_metadata = f"""<?METADATA><?NO_FILES>{len(input_files)}</?NO_FILES><?FILES>{"".join([
        f"<?FILE><?NAME>{j}</?NAME><?SIZE>{os.path.getsize(i)}</?SIZE></?FILE>" for i, j in input_files
    ])}</?FILES></?METADATA>""".encode('utf-8')
    with fp:
        fp.write(archive_metadata)
        for i, j in input_files:
            append_file_to_archive(i, fp)
    pass


def run_list_content(target_archive: str):
    """
    prints a list of files inside target_archive
    then exits program

    :param target_archive: the path to an already created archive
    :return: void
    """
    print("\n".join(f"{i}: size: {j}" for i, j in get_archive_content(target_archive)[1]))
    pass


def run_full_unpack(target_archive: str, target_folder: str):
    """
    creates target_folder where it unpacks all content of target_archive
    then exits program

    :param target_archive: the path to an already created archive
    :param target_folder: the path to the unpack location directory; should not already exist
    :return: void
    """
    prepare_archive_unpacking(target_archive, target_folder)
    metadata_length, files = get_archive_content(target_archive)
    with open(target_archive, "rb") as fp:
        fp.read(metadata_length)
        for file, size in files:
            unpack_file(file=target_folder + "/" + file, size=int(size), fp=fp)
    pass


def run_unpack(target_archive: str, target_folder: str, *target_files: str):
    """
    creates target_folder where it unpacks listed target_files from target_archive
    then exits program

    :param target_archive: the path to an already created archive
    :param target_folder: the path to the unpack location directory; should not already exist
    :param target_files: a list of files inside target_archive
    :return: void
    """
    prepare_archive_unpacking(target_archive, target_folder)
    metadata_length, files = get_archive_content(target_archive)
    possible_files = [x for x, y in files]
    for i in target_files:
        if i not in possible_files:
            raise CustomError(f"{i} nu se afla in urmatoarele fisiere:{', '.join(possible_files)}]")
    with open(target_archive, "rb") as fp:
        fp.read(metadata_length)
        for file, size in files:
            if file in target_files:
                unpack_file(file=target_folder + "/" + file, size=int(size), fp=fp)
            else:
                empty_read_archive(size=int(size), fp=fp)
    pass
