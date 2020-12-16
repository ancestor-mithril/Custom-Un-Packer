"""A7 - Custom (un)-packer

Creati un tool de impachetare/despachetare fisiere. Tool-ul manipuleaza arhive create dupa
un format definit de dezvoltator. Un set minim de comenzi pe care va trebui sa le stie tool-ul
sunt: creare_arhiva ( cu param 1 fisier, 1 director sau o lista de fisiere) - creaza o arhiva
Listare_continut - va lista fisierele din interiorul arhivei si size-ul lor
Full_unpack ( cu parametru un folder destinatie ) - dezarhiveaza toata arhiva
Unpack ( lista de fisiere in folder de output ) - dezarhiveaza doar fisierele respective
!!! nu se vor folosi biblioteci python 3rd party si nu aveti voie sa folositi zipFile (nu este nevoie
de compresie)
"""


import sys
from utils import error_print, CustomError
from functions import run_help, run_list_content, run_create_archive, run_full_unpack, run_unpack


def run(command: str):
    """
    the script arguments match the following structure:
    a_seven.py command [target_archive [ [target_folder] [file_1 [file_2...]] ] ]

    run processes sys.argv arguments and calls required functions; raises exceptions if arguments do not match the
    above mentioned format or command is not recognized

    :param command: first argument of `a_seven`; should be "--help", "-create_archive", "-list_content", "-full_unpack",
                    or "-unpack"
    :return: void
    """
    if command == "--help":
        run_help()
        exit(0)
    try:
        target_archive = sys.argv[2]
    except IndexError:
        raise CustomError("Target archive not mentioned")
    if command == "-list_content":
        run_list_content(target_archive)
        exit(0)
    try:
        target_folder = sys.argv[3]
    except IndexError:
        raise CustomError("Target location not mentioned")
    if command == "-create_archive":
        run_create_archive(target_archive, *sys.argv[3:])
        exit(0)
    if command == "-full_unpack":
        run_full_unpack(target_archive, target_folder)
        exit(0)
    try:
        target_files = sys.argv[4:]
    except IndexError:
        raise CustomError("Target files not mentioned")
    if command == "-unpack":
        run_unpack(target_archive, target_folder, *target_files)
        exit(0)
    raise CustomError("Invalid first argument. Run `python a_seven.py --help` for help")


if __name__ == "__main__":
    # sys.argv[1:] = ["--help"]
    # sys.argv[1:] = ["-create_archive", "./test.archive", "./utils"]
    # sys.argv[1:] = ["-list_content", "./test.archive"]
    # sys.argv[1:] = ["-create_archive", "./test2.archive", "./LICENSE", "./test.archive"]
    # sys.argv[1:] = ["-full_unpack", "./test2.archive", "./test_unpack_2"]
    # sys.argv[1:] = ["-unpack", "./test.archive", "./test_unpack_4", "/custom_error.py", "/open_2.py"]
    if len(sys.argv) < 2:
        error_print("Invalid syntax. Run `python a_seven.py --help` for help")
    try:
        run(sys.argv[1])
    except CustomError as e:
        error_print(f"Error: {e}")
        exit("Error")
    except Exception as e:
        error_print(f"Other error: {e}")
        exit("Error 2")


