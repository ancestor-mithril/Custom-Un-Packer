import errno
import unittest
import os

from functions import run_create_archive, run_full_unpack
from utils import open_2, are_folders_equal
import shutil  # used for easily deleting directory along with the entire subtree


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


def create_test_folders(folder: str):
    """
    creates test folders

    :param folder: folder name
    :return:
    """
    create_folder(f"./test")
    create_folder(f"./test/{folder}")
    create_folder(f"./test/{folder}/inside_dir")

    with open_2(
            (f"./test/{folder}/file1", "w"), (f"./test/{folder}/file2", "w"),
            (f"./test/{folder}/file3", "w"), (f"./test/{folder}/inside_dir/file4", "w")
    ) as fps:
        for i in fps:
            i.write("test")


class CustomUnPackerTester(unittest.TestCase):
    def test_create_archive_from_directory(self):
        target_archive = "./test/test.archive"
        create_test_folders("test_folder")
        create_test_folders("archived_folder")
        run_create_archive(target_archive, "./test/test_folder")
        run_full_unpack(target_archive, "./test/archived_folder")
        self.assertTrue(are_folders_equal("./test/archived_folder", "./test/test_folder"))
        shutil.rmtree("./test")
