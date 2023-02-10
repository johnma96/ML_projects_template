# This module is used to develop functions that read files containing SQL
# Queries.

import warnings

from .absolute_paths import AbsPaths


def read_sql(file_name: str, file_path: str = None) -> str:
    """
    It reads a plain text file with a .sql extension. Allow only the filename
    to be passed, in which case it tries to search for that file in one of the
    package's subpackages using the AbsPaths class and a default depth level of 5.

    Parameters
    ----------
    file_name : str
        Name of the file to read
    file_path : str, optional
        Absolute path of the file to read, by default None

    Returns
    -------
    str
        Query read content in the file
    """

    abs_path_manager = AbsPaths()

    if file_path is None:
        file_path = abs_path_manager.get_abs_path_file(file_name)

    if isinstance(file_path, list):
        msg = f"""
        2 or more files with the same name were found, the query that has 
        been read is the one for the location {file_path[0]}
        """
        warnings.warn(msg)

        file_path = file_path[0]

    with open(file_path, "r") as f:
        return f.read()
