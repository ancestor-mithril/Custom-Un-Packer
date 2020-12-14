import errno
import unittest
import os
from archive import get_archive_content
from functions import run_create_archive, run_full_unpack, run_unpack
from utils import open_2, are_folders_equal, get_files_from_directory, are_files_equal, error_print
import shutil  # used for easily deleting directory along with the entire subtree

from utils.utils import get_local_path_of_files_from_directory


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
        """
        creates test folder, runs create_archive on it and full_unpack, then verifies equality of initial and unpacked
        should runtime error occur, test fails
        """
        target_archive = "./test/test.archive"
        create_test_folders("test_folder")
        # create_test_folders("archived_folder")
        no_error = True
        ok = True
        try:
            run_create_archive(target_archive, "./test/test_folder")
            # run_create_archive(target_archive, "./utils.rar")
            run_full_unpack(target_archive, "./test/archived_folder")
            ok = are_folders_equal("./test/archived_folder", "./test/test_folder")
        except Exception as e:
            no_error = False
            error_print(e)
        shutil.rmtree("./test")
        self.assertTrue(no_error, "Runtime error")
        self.assertTrue(ok, "Folders are not equal")

    def test_create_archive_from_files(self):
        """
        creates test folder, runs create_folder on some files, full unpack and verifies equality of used files
        should runtime error occur, test fails
        """
        target_archive = "./test/test.archive"
        create_test_folders("test_folder")
        # create_test_folders("archived_folder")
        target_files = ["./test/test_folder/file1", "./test/test_folder/inside_dir/file4"]
        no_error = True
        ok = True
        try:
            run_create_archive(target_archive, *target_files)
            run_full_unpack(target_archive, "./test/archived_folder")
            unpacked_files = get_files_from_directory("./test/archived_folder")
            if len(target_files) != len(unpacked_files):
                ok = False
            for i, j in zip(target_files, unpacked_files):
                if not are_files_equal(i, j):
                    ok = False
        except Exception as e:
            error_print(e)
            no_error = False
        shutil.rmtree("./test")
        self.assertTrue(no_error, "Runtime error")
        self.assertTrue(ok, "Content of files are not equal")

    # def test_list_content(self):
    #     """
    #     creates test folder, then archives it and verifies list_archive_content to be same as model
    #     """
    #     target_archive = "./test/test.archive"
    #     create_test_folders("test_folder")
    #     correct_answer = [
    #         "\\file1", "\\file2", "\\file3", "\\inside_dir\\file4"
    #     ]
    #     list_archive_content = []
    #     no_error = True
    #     ok = True
    #     try:
    #         run_create_archive(target_archive, "./test/test_folder")
    #         list_archive_content = [x for x, y in get_archive_content(target_archive)[1]]
    #     except Exception as e:
    #         error_print(e)
    #         no_error = False
    #     shutil.rmtree("./test")
    #     self.assertTrue(no_error, "Runtime error")
    #     self.assertEqual(correct_answer, list_archive_content, "Listed content is not the same")
    #
    # def test_unpack(self):
    #     """
    #     creates test folder, archives it and tests for custom unpack to work as expected
    #     """
    #     target_archive = "./test/test.archive"
    #     create_test_folders("test_folder")
    #     target_files = ["\\file1", "\\inside_dir\\file4"]
    #     unpacked_files = []
    #     no_error = True
    #     ok = True
    #     try:
    #         run_create_archive(target_archive, "./test/test_folder")
    #         run_unpack(target_archive, "./test/archived_folder", *target_files)
    #         unpacked_files = get_local_path_of_files_from_directory("./test/archived_folder")
    #     except Exception as e:
    #         error_print(e)
    #         no_error = False
    #     shutil.rmtree("./test")
    #     self.assertTrue(no_error, "Runtime error")
    #     self.assertEqual(target_files, unpacked_files, "Unpacked files are not the expected ones")
