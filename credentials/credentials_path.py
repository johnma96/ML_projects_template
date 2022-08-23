import os


class Credentials:
    """
    Class to manipulate the absolute and relative paths from 'credentials' folder
    """

    def __init__(self) -> None:
        self.path_parent = os.path.dirname(__file__)
        self.sep = os.path.sep

    def get_path(self) -> str:
        return self.path_parent + self.sep
