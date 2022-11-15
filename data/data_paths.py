import os


class Data:
    """
    Class to manipulate the absolute and relative paths from 'data' folder
    """

    def __init__(self) -> None:
        self.path_parent = os.path.dirname(__file__)
        self.sep = os.path.sep

    def get_path(self, type: str) -> str:
        """
        Get the absolute path of the data sub-package.        

        Parameters
        ----------
        type :{'raw', 'interim', 'processed', 'external'} str
            Name of folder to seek data.

        Returns
        -------
        str
            Absolute path until the data sub-package.
        """
        if type.lower() == "raw":
            path = self.path_parent + self.sep + "raw"
        elif type.lower() == "interim":
            path = self.path_parent + self.sep + "interim"
        elif type.lower() == "processed":
            path = self.path_parent + self.sep + "processed"
        else:
            path = self.path_parent + self.sep + "external"
        return path + self.sep
