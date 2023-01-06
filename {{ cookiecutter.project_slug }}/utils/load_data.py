import os
import pandas as pd
import warnings

from google.oauth2   import service_account
from .absolute_paths import Abs_paths


class Load_data:
    """
    Class to load data in a Pythonic way, this from different information 
    sources: 
        - Data in the data subfolder.
        - Called from some RBDM such as BigQuery, MySQL, Postgres, etc.

    Attributes
    ----------
    path_credentials : str
        Absolute path to the credentials subfolder

    abs_ : Abs_paths
        "Abs_path" type object used to find the files to be loaded

    Methods
    -------
    from_BigQuery(query, path_credentials=None, name_file=None, 
                project_id='dolphin-prod')
        Read data directly from GCP BigQuery Service
    from_csv(path=None, type=None, name_file=None, **kwargs)
        Read .csv files from sub-subfolders within data subfolder
    from_excel(path=None, type=None, name_file=None, **kwargs)
        Read excel files from sub-subfolders within data subfolder
    """
    
    def __init__(self) -> None:
        self.abs_ = Abs_paths()
        self.path_credentials = self.abs_.get_abs_path_folder('credentials')
        try:
            path_credentials = self.path_credentials + 'credentials_bq.json'
            self.credentials_bq = service_account.Credentials.from_service_account_file(
                path_credentials
            )
        except: 
            warnings.warn("The object was not able to set BigQuery credentials" 
                        "using the 'credentials_bq.json' file inside the 'credentials' folder")

    def from_BigQuery(self,
                    query: str,
                    path_credentials: str = None,
                    name_file: str = None,
                    project_id: str = "dolphin-prod",
                ) -> pd.DataFrame:
        """
        Load data directly from the Google Cloud Platform BigQuery service.

        Parameters
        ----------
        query : str
            Query to be read and then load data
        path_credentials : str, optional
            Credential's path to do connection with GCP (It's recommended use a
            service account). By default is None. If it's not passed you can 
            set name_file parameter to search credential within credentials 
            subfolder
        name_file : str, optional
            File name, json type that has credentials to connect with some GCP 
            project, by default None
        project_id : str, optional
            GCP project ID, by default "dolphin-prod"

        Returns
        -------
        pd.DataFrame
            Dataframe with data loaded from the GCP project

        Raises
        ------
        ValueError
            If neither a path nor a name is supplied to search for credentials 
            within the credentials subfolder
        """

        if path_credentials is None:
            try:
                path_credentials = self.path_credentials + name_file
            except:
                raise ValueError(
                    "Need to provide a filename to search within the credentials folder"
                )
        try:
            self.credentials_bq = service_account.Credentials.from_service_account_file(
                path_credentials
            )
        except:
            try:
                path_credentials = self.abs_.get_abs_path_file(name_file)
                self.credentials_bq = service_account.Credentials.from_service_account_file(
                path_credentials
            )

            except:
                raise ValueError('BigQuery connection credentials could not be established')


        df = pd.read_gbq(query=query, project_id=project_id,
                         credentials=self.credentials_bq)

        return df

    def from_csv(self, path: str = None, type: str = None, 
                name_file: str = None, **kwargs) -> pd.DataFrame:
        """
        Call data using pandas.read_csv method. To get data directly from data
        folder just select the type of folder and set file's name. 
        
        You can pass all arguments of pandas native method.

        Parameters
        ----------
        path : str, optional
            File path, by default None. If None, the file is expected to be in 
            the data subfolder
        type :{None, 'raw', 'interim', 'processed', 'external'} str, optional
            Name of the sub-subfolder within the data subfolder, by default 
            None. Keep None if you provide a path to the file
        name_file : str, optional
            Name of the file to be searched within the data folder, by default 
            None
        **kwargs : 
            Additional keywords passed to pandas.read_csv() method

        Returns
        -------
        pd.DataFrame
            Dataframe with loaded data
        """
        try: 
            path_to_search = self.__build_path(path, type, name_file)
            df = pd.read_csv(filepath_or_buffer=path_to_search, **kwargs)
        except:
            warnings.warn(message="The file is not within the searched subfolder type."
                                " Will be searched using only the name." 
                                " Make sure it is the file you are looking for.")
            path_to_search = self.abs_.get_abs_path_file(name_file)
            df = pd.read_csv(filepath_or_buffer=path_to_search, **kwargs)

        return df

    def from_excel(self, path: str = None, type: str = None, 
                    name_file: str = None, **kwargs) -> pd.DataFrame:
        """
        Call data using pandas.read_excel method. To get data directly from data
        folder just select the type of folder and set file's name. 
        
        You can pass all arguments of pandas native method.

        Parameters
        ----------
        path : str, optional
            _description_, by default None
        type :{None, 'raw', 'interim', 'processed', 'external'} str, optional
            Name of the sub-subfolder within the data subfolder, by default 
            None. Keep None if you provide a path to the file
        name_file : str, optional
            Name of the file to be searched within the data folder, by default 
            None
        **kwargs : 
            Additional keywords passed to pandas.read_excel() method

        Returns
        -------
        pd.DataFrame
            Dataframe with loaded data
        """

        try: 
            path_to_search = self.__build_path(path, type, name_file)
            df = pd.read_excel(io=path_to_search, **kwargs)
        except:
            warnings.warn(message="The file is not within the searched subfolder type."
                                " Will be searched using only the name." 
                                " Make sure it is the file you are looking for.")
            path_to_search = self.abs_.get_abs_path_file(name_file)
            df = pd.read_excel(io=path_to_search, **kwargs)

        return df

    def __build_path(self, path: str = None, type: str = None,
                     name_file: str = None) -> str:
        """
        Build the path to find the file in which the data to be loaded is 
        located.

        Parameters
        ----------
        path : str, optional
            File path, by default None. If None, the file is expected to be in 
            the data subfolder
        type :{None, 'raw', 'interim', 'processed', 'external'} str, optional
            Name of the sub-subfolder within the data subfolder, by default 
            None. Keep None if you provide a path to the file
        name_file : str, optional
            Name of the file to be searched within the data folder, by default 
            None

        Returns
        -------
        str
            File path passed by the user or absolute file path within the data 
            subfolder

        Raises
        ------
        KeyError
            If a path to the file is not provided, or if you do not provide a 
            correct name of the subfolders within the data folder, or if you do 
            not provide the correct name of any file
        """
        type_options = ['raw', 'interim', 'processed', 'external']


        if all([True if option is None else False for option in (path, type, name_file)]):
            raise KeyError("You did not provide information for the search")

        elif (path is not None) and (type is None) and (name_file is None):
            path_to_search = path
        
        elif (path is None) and (type in type_options) and (name_file is not None):
            path_to_search = self.abs_.get_abs_path_folder(folder_name=type, deep=2)
            path_to_search += name_file

        elif (path is None) and not(type in type_options) and (name_file is not None):
            first_part_msg = "The subfolder passed does not exist within data."
            if type is None:
                first_part_msg = ''
            warnings.warn(message=first_part_msg+ 
                                    " The file will be searched using only the name." 
                                    " Make sure it is the file you are looking for.")
            path_to_search = self.abs_.get_abs_path_file(name_file)

        else:
            raise KeyError(
                "Cannot set a path to the file with the given parameter settings"
            )

        return path_to_search
