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
import os
from utils import error_print, color_print, CustomError


def run(command: str):
    """
    the script arguments match the following structure:
    a_seven.py command [target_archive [ [target_folder] [file_1 [file_2...]] ] ]

    :param command: first argument of `a_seven`; should be "--help", "-create_archive", "-list_content", "-full_unpack",
                    or "-unpack"
    :return: void
    """


if __name__ == "__main__":
    if len(sys.argv) < 2:
        error_print("Invalid syntax. Run `python a_seven.py --help` for help")
    try:
        run(sys.argv[1])
    except CustomError as e:
        error_print(f"Error:{e}")
        exit("Error")
    except Exception as e:
        error_print(f"Other error: {e}")
        exit("Error 2")


