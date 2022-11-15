#Script for ingesting data from different sources

import pandas as pd

from google.oauth2 import service_account

from data        import Data
from credentials import Credentials


class Load_data:
    def __init__(self) -> None:
        self.path_credentials = Credentials().get_path()

    def from_BigQuery(
        self,
        query: str,
        path_credentials: str = None,
        name_file: str = None,
        project_id: str = "dolphin-prod",
    ) -> pd.DataFrame:

        if path_credentials is None:
            try:
                path_credentials = self.path_credentials + name_file
            except:
                raise ValueError(
                    "Need to provide a filename to search within the credentials folder"
                )

        credentials = service_account.Credentials.from_service_account_file(
            path_credentials
        )

        df = pd.read_gbq(query=query, project_id=project_id, credentials=credentials)

        return df

    def from_csv(
        self, path: str = None, type: str = None, name_file: str = None, **kwargs
    ) -> pd.DataFrame:
        """
        Call data using pandas.read_csv. To get data from data
        folder just select the type of folder and set file's name
        """
        path_to_search = self.__build_path(path, type, name_file)
        df = pd.read_csv(filepath_or_buffer=path_to_search, **kwargs)

        return df

    def from_excel(
        self, path: str = None, type: str = None, name_file: str = None, **kwargs
    ) -> pd.DataFrame:
        """
        Call data using pandas.read_excel. To get data from data
        folder just select the type of folder and set file's name
        """
        path_to_search = self.__build_path(path, type, name_file)
        df = pd.read_excel(io=path_to_search, **kwargs)

        return df

    def __build_path(self, path, type, name_file) -> str:
        """
        Build path from data folder
        """
        # Getting the path of data folder within project and passing to read excel
        if path is None and not (type is None) and not (name_file is None):
            folder_to_search = type
            path_to_search = Data().get_path(type=folder_to_search)
            path_to_search += name_file
        elif not (path is None) and (type is None) and (name_file is None):
            path_to_search = path
        else:
            raise KeyError(
                "You do not provided a search path, you must necessarily type a folder that is inside the 'data' folder, in which the excel file you want to open will be"
            )
        return path_to_search
