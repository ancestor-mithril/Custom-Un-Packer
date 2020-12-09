import errno
import unittest
import os
from utils import open_2
import shutil


def create_folder(folder_path: str):
    """
    creates folder but does not throw error if already exists

    :param folder_path: valid path towards folder
    :return:
    """
    try:
        os.makedirs(folder_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def create_test_folders():
    """
    creates test folders

    :return: void
    """
    create_folder("./test")
    create_folder("./test/test_folder")
    create_folder("./test/test_folder/inside_dir")

    with open_2(
            ("./test/test_folder/file1", "w"), ("./test/test_folder/file2", "w"),
            ("./test/test_folder/file3", "w"), ("./test/test_folder/inside_dir/file4", "w")
    ) as fps:
        for i in fps:
            i.write("test")


class CustomUnPackerTester(unittest.TestCase):
    def test_test(self):
        create_test_folders()
        shutil.rmtree("./test")
