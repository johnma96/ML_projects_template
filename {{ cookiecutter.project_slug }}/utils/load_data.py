import warnings
import pandas as pd

from .make_connection import MakeConnection
from .read_sql_file import read_sql


class LoadData(MakeConnection):
    """
    Class to load data in a Pythonic way, this from different information
    sources:
        - Data in the data subfolder.
        - Called from some RBDM such as BigQuery, MySQL, Postgres, etc.

    Attributes
    ----------
    file_credentials_path: str
        Absolute path to the .json credentials file to BigQuery. Only if the
        with_gbq() method is used. Inherited from MakeConnection class
    credentials_bq: service_account
        Connection object to BigQuery using a service account. Only if the
        with_gbq() method is used. Inherited from MakeConnection class
    max_level: int
        Maximum level of depth within the package, in which it seeks to establish
        the absolute paths. Inherited from the AbsPaths class

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

    def __init__(
        self,
        file_credentials_path: str = None,
        file_credentials_name="credentials_bq.json",
        type_rdbms: str = "bigquery",
        max_level: int = 5,
    ) -> None:

        # Set max depth to handle routes
        super().__init__(max_level=max_level)

        try:
            # Establish connection with BigQuery service using MakeConnection class
            if type_rdbms == "bigquery":
                self.with_gqb(
                    file_credentials_path=file_credentials_path,
                    file_credentials_name=file_credentials_name,
                )
        except (FileNotFoundError, ValueError):
            warnings.warn("Your instance is not connected with BigQuery")

    def from_bigquery(
        self,
        query: str,
        file_credentials_path: str = None,
        file_credentials_name: str = None,
        project_id: str = "dolphin-prod",
        **kwargs
    ) -> pd.DataFrame:
        """
        Load data directly from the Google Cloud Platform BigQuery service.

        Parameters
        ----------
        query : str
            Query to be read and then load data. You can pass a query directly
            or the name of the .sql file that contains it.
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
        **kwargs: dict, optional
            Extra arguments (such as a google BigQuery connection object) to be
            passed to pandas_gbq's to_gbq function

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

        if ".sql" in query:
            query = read_sql(file_name=query)

        # Make connection with BigQuery service
        if not (file_credentials_name is None) or not (file_credentials_path is None):
            self.with_gqb(
                file_credentials_path=file_credentials_path,
                file_credentials_name=file_credentials_name,
            )

        df = pd.read_gbq(
            query=query, project_id=project_id, credentials=self.credentials_bq
        )

        return df

    def from_mysql(self): pass 

    def from_psql(self): pass

    def from_csv(
        self,
        file_path: str = None,
        data_type: str = "raw",
        file_name: str = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Call data using pandas.read_csv method. To get data directly from data
        folder just select the type_data of folder and set file's name.

        You can pass all arguments of pandas native method.

        Parameters
        ----------
        path : str, optional
            File path, by default None. If None, the file is expected to be in
            the data subfolder
        type :{'raw', 'interim', 'processed', 'external'} str, optional
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

        file_path = self.__build_path(
            file_path=file_path, data_type=data_type, file_name=file_name
        )

        return pd.read_csv(filepath_or_buffer=file_path, **kwargs)

    def from_excel(
        self,
        file_path: str = None,
        data_type: str = "raw",
        file_name: str = None,
        **kwargs
    ) -> pd.DataFrame:
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

        file_path = self.__build_path(
            file_path=file_path, data_type=data_type, file_name=file_name
        )

        return pd.read_excel(io=file_path, **kwargs)

    def __build_path(
        self, file_path: str = None, data_type: str = "raw", file_name: str = None
    ) -> str:
        """
        Build the path to find the file in which the data to be loaded is
        located.

        Parameters
        ----------
        file_path : str, optional
            File path, by default None. If None, the file is expected to be in
            the data subfolder
        type_data :{'raw', 'interim', 'processed', 'external'} str, optional
            Name of the sub-subfolder within the data subfolder, by default
            None. Keep None if you provide a path to the file
        file_name : str, optional
            Name of the file to be searched within the data folder, by default
            None

        Returns
        -------
        str
            File path passed by the user or absolute file path within the data
            subfolder

        Raises
        ------
        FileNotFoundError
            if the requested file exists in a different path than the data_type
            passed
        """
        if file_path is None:
            file_path = self.get_abs_path_file(file_name=file_name)

            # Case in which are multiple files with same name in the package
            if isinstance(file_path, list):
                try:
                    file_path_end = [path for path in file_path if data_type in path][0]
                except:
                    msg = """File wasn't found within {} folder. Was found in other paths: \n{}""".format(
                        data_type, "\n".join(file_path)
                    )
                    raise FileNotFoundError(msg)

                file_path = file_path_end

            # The file isn't within the type_data folder gave
            if not (data_type in file_path):
                msg = """File wasn't found within {} folder. Was found in other paths: \n{}""".format(
                    data_type, file_path
                )
                raise FileNotFoundError(msg)

        return file_path