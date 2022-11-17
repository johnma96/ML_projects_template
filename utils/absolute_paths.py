import os

from glob   import glob
from typing import Union

class Abs_paths:
    """
    Class intended for the manipulation of the absolute paths of the packet.

    Attributes
    ----------
    parent_path : str
        Absolute package path
    option_paths : dict
        Dictionary with absolute paths of subpackages up to the fifth level 
        of depth


    Methods
    -------
    get_absolute_path(self, folder_name, deep=1)
        Gets the absolute path of the searched folder according to the 
        depth level.
    """
    __exclude_folders = ['.vscode', '__pycache__', 'venv', 'env',
                                '.venv', '.env','.git']

    def __init__(self, max_level: int = 5) -> None:
        """
        Parameters
        ----------
        max_level : int, optional
            Maximum level of depth within the parent package, by default 5

        """

        self.parent_path = os.path.abspath(os.path.join(f'..{os.sep}..'))
        self.__build_paths(max_level)

    def get_absolute_path(self, folder_name: str, deep: int = 1) -> Union[str, list]:
        """
        Gets the absolute path of the searched object according to the depth 
        level.

        Parameters
        ----------
        object_name : str
            Searched object name
        deep : int, optional
            Depth level to search for the object, by default 1

        Returns
        -------
        str | list
            Path or list of paths for the searched object

        Raises
        ------
        ValueError
            If the passed object name does not exist within the passed deep
        """
        if folder_name in self.__exclude_folders:
            raise ValueError('This folder is excluded from searching')

        obj_lev = []
        paths_lev = []

        for option in self.option_paths[deep]:
            obj_lev.append(option.split(os.sep)[-2])
            paths_lev.append(option)
        
        if folder_name in obj_lev:

            possible_index = [index for (index, item) in enumerate(obj_lev) 
                                if item == folder_name]
            
            if len(possible_index) == 1:
                return paths_lev[possible_index[0]]
            else:
                return [paths_lev[index] for index in possible_index]
        else:
            raise ValueError(f"The object doesn't exist in the {deep} level")

    def __build_paths(self, max_level) -> dict:
        """
        Build a dictionary with paths for depth levels from 1 to max_level.

        Returns
        -------
        dict
            Dictionary with the absolute paths of each level until the 
            max_level
        """

        def paths_at_level(level: int) -> list:
            """
            Gets the absolute paths of the folders at the searched level.

            Parameters
            ----------
            level : int
                Level deep into parent directory to get paths

            Returns
            -------
            list
                List of routes at the level sought
            """
            
            options = glob(self.parent_path+os.sep+'*\\'*level)
            final_paths = []
            for option in options:
                subfolders = option.split(os.sep)
                list_subs = subfolders[-(level+1):-1]
                if any([element in self.__exclude_folders for element in list_subs]):
                    continue
                else: final_paths.append(option)
            return final_paths

        dictionary_paths = {level:paths_at_level(level) for level in 
                                                        range(0,max_level+1)}

        self.option_paths = dictionary_paths

    def get_exclude_folders(self) -> list:
        """
        Get a list of folders whose absolute path cannot be obtained

        Returns
        -------
        list
            List of excluded folders
        """
        
        return self.__exclude_folders
