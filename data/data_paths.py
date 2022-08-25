import os


class Data:
    """
    Class to manipulate the absolute and relative paths from 'data' folder
    """

    def __init__(self) -> None:
        self.path_parent = os.path.dirname(__file__)
        self.sep = os.path.sep

    def get_path(self, type: str) -> str:
        if type.lower() == "raw":
            path = self.path_parent + self.sep + "raw"
        elif type.lower() == "processed":
            path = self.path_parent + self.sep + "processed"
        else:
            path = self.path_parent + self.sep + "archive"
        return path + self.sep
