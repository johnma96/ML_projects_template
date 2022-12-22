import os
import pyprojroot

from glob   import glob
from typing import Union

class Abs_paths:
    """
    Class intended for the manipulation of the absolute paths of the packet.

    Attributes
    ----------
    parent_path : str
        Absolute package path
    option_paths_folders : dict
        Dictionary with absolute paths of subpackages up to the fifth level 
        of depth
    option_paths_files : dict
        Dictionary with absolute paths of subpackages up to the fifth level 
            of depth


    Methods
    -------
    get_absolute_path(self, folder_name, deep=1)
        Gets the absolute path of the searched folder according to the 
        depth level.
    """
    __excluded_folders = ['.vscode', '__pycache__', 'venv', 'env',
                                '.venv', '.env','.git']
    __excluded_files = ['__init__.py', 'cpython-39.pyc']
    __excluded_endings = ['cpython-39.pyc']

    def __init__(self, max_level: int = 5) -> None:
        """
        Parameters
        ----------
        max_level : int, optional
            Maximum level of depth within the parent package, by default 5

        """

        self.parent_path = pyprojroot.here().__str__()
        self.__build_paths(max_level)

    def get_abs_path_file(self, file_name: str, deep: int = 5) -> Union[str, list]:

        """
        Gets the absolute path of the searched folder according to the depth 
        level.

        Parameters
        ----------
        file_name : str
            Searched file name
        deep : int, optional
            Max depth level to search for the file, by default 5

        Returns
        -------
        str | list
            Path or list of paths for the searched object

        Raises
        ------
        ValueError
            If the passed object name does not exist within the passed deep
        """
        if file_name in self.__excluded_files:
            raise ValueError('This file is excluded from searching')

        file_lev = []
        paths_lev = []

        for level in range(0, deep+1):
            for option in self.option_paths_files[level]:
                file_lev.append(option.split(os.sep)[-1])
                paths_lev.append(option)
        
        if file_name in file_lev:
            possible_index = [index for (index, item) in enumerate(file_lev) 
                                if item == file_name]
            
            if len(possible_index) == 1:
                return paths_lev[possible_index[0]]
            else:
                return [paths_lev[index] for index in possible_index]
        else:
            raise ValueError(f"The file is not found in a depth up to {deep} levels")

    def get_abs_path_folder(self, folder_name: str, deep: int = 5) -> Union[str, list]:

        """
        Gets the absolute path of the searched folder according to the depth 
        level.

        Parameters
        ----------
        folder_name : str
            Searched folder name
        deep : int, optional
            Max depth level to search for the folder, by default 5

        Returns
        -------
        str | list
            Path or list of paths for the searched object

        Raises
        ------
        ValueError
            If the passed object name does not exist within the passed deep
        """
        if folder_name in self.__excluded_folders:
            raise ValueError('This folder is excluded from searching')

        folder_lev = []
        paths_lev = []

        for level in range(1, deep+1):
            for option in self.option_paths_folders[level]:
                folder_lev.append(option.split(os.sep)[-2])
                paths_lev.append(option)
        
        if folder_name in folder_lev:
            possible_index = [index for (index, item) in enumerate(folder_lev) 
                                if item == folder_name]
            
            if len(possible_index) == 1:
                return paths_lev[possible_index[0]]
            else:
                return [paths_lev[index] for index in possible_index]
        else:
            raise ValueError(f"The folder is not found in a depth up to {deep} levels")

    def __build_paths(self, max_level) -> dict:
        """
        Build a dictionary with paths for depth levels from 1 to max_level.

        Returns
        -------
        dict
            Dictionary with the absolute paths of each level until the 
            max_level
        """

        def paths_at_level(level: int, type: str = 'folders') -> list:
            """
            Gets the absolute paths of the folders at the searched level.

            Parameters
            ----------
            level : int
                 Level deep into parent directory to get paths
            type : {'folders', 'files'}, optional
                Swith the search between paths of folders or files, 
                by default 'folders'

            Returns
            -------
            list
                List of routes at the level sought

            Raises
            ------
            ValueError
                if you supply some type other than 'folder' or 'file'
            """
            if level == 0:
                options = glob(self.parent_path)
            else: 
                options = glob(self.parent_path+os.sep+f'{os.sep}*'*level)

            if type == 'folders':
                options = [opt+os.sep for opt in options if (
                                os.path.isdir(opt) and 
                                opt.split(os.sep)[-1] not in self.__excluded_folders
                            )
                        ]

            elif type == 'files':
                options = [opt for opt in options if (
                                (os.path.isfile(opt)) 
                                and
                                (opt.split(os.sep)[-1] not in self.__excluded_files)
                                and
                                not(any([opt.endswith(end) for end in self.__excluded_endings]))
                            )
                        ]
            else:
                raise ValueError('You can only select between folders and files')

            return options

        dict_paths_folders = {level:paths_at_level(level, type='folders') for level in 
                                                        range(0,max_level+1)}
        dict_paths_files = {level:paths_at_level(level, type='files') for level in 
                                                        range(0,max_level+1)}

        self.option_paths_folders = dict_paths_folders
        self.option_paths_files = dict_paths_files

    def get_excluded_folders(self) -> list:
        """
        Get a list of folders whose absolute path cannot be obtained

        Returns
        -------
        list
            List of excluded folders
        """
        
        return self.__excluded_folders
