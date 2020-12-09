"""
Class used for opening a variable number of files and writing in them
"""


from typing import List, Tuple


class open_2(object):
    def __init__(self, *files: Tuple[str, str]):
        """

        :param files: a list of paths to files
        """
        self.fps = []
        self.files = []
        for file in files:
            self.fps.append(None)
            self.files.append(file)

    def __enter__(self):
        """
        triggers when opened with :keyword: "with"
        opens file pointers for each file

        :return: returns opened file pointers
        """
        for i in range(len(self.fps)):
            self.fps[i] = open(self.files[i][0], self.files[i][1])
        return self.fps

    def __exit__(self, type, value, traceback):
        """
        triggers when exiting from :keyword: "with"
        closes opened file pointers
        :return:
        """
        for i in range(len(self.fps)):
            self.fps[i].close()
