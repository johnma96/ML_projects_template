import warnings
import pandas as pd

from .make_connection import MakeConnection


class SaveData(MakeConnection):
    """
    Class created to save data in different RDBMS (MySQL, Postgres, BigQuery, etc)

    By default it tries to create a connection to BigQuery. If this is not the 
    desired behavior a credentials file must be set to a different RDBMS during 
    instance creation.

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
    data_to_gbq(table, project_bq="dolphin-prod", if_exists="append")
        Stores data within a BigQuery project
    data_to_msql():
        Stores data within a MySQL-like database. Need to be implemented
    data_to_psql():
        Stores data within a Postgres-like database. Need to be implemented

    Warns
    -----
    UserWarning
        If the instance fails to connect to the RDBMS during its creation

    """

    def __init__(
        self,
        file_credentials_path: str = None,
        file_credentials_name = "credentials_bq.json",
        type_rdbms: str = 'bigquery',
        max_level: int = 5
    ) -> None:
        """
        Parameters
        ----------
        type_rdbms: {'bigquery', 'mysql', 'postgres'}
            Type of RDBMS to which the connection will be made.
        file_credentials_path : str, optional
            Absolute path to the .json file containing the connection 
            credentials, by default None
        file_credentials_name : str, optional
            The name of the .json file with the BigQuery connection credentials, 
            by default "credentials_bq.json". This option is used only when the 
            file is found in any of the package folders up to the max_level given 
            in the instance and an absolute path has not been passed, if the path 
            is supplied it will take precedence

            It is recommended that this file be called credentials_bq.json and 
            that it be stored in the credentials folder.
        max_level : int, optional
            Maximum level of depth to perform the construction of routes in the 
            package, by default 5.

            This is done using the methods of the AbsPath class which allows 
            handling paths within the package.
        """

        # Set max depth to handle routes 
        super().__init__(max_level=max_level)
        
        try:
            # Establish connection with BigQuery service using MakeConnection class
            if type_rdbms == "bigquery":
                self.with_gqb(file_credentials_path=file_credentials_path, 
                            file_credentials_name=file_credentials_name)
        except (FileNotFoundError, ValueError):
            warnings.warn("Your instance is not connected with BigQuery")


    def data_to_gbq(
        self,
        data: pd.DataFrame,
        table: str,
        project_bq: str = "dolphin-prod",
        if_exists: str = "append",
        **kwargs
    ) -> None:
        """
        It uses the to_gbq method of the pandas_gbq library to store data.

        By default, it uses BigQuery credentials to perform data storage.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame containing the data to be stored
        table : str
            Name of table to be written, in the form ``dataset.tablename``.
        project_bq : str, optional
            Google BigQuery Account project ID. Optional when available from
            the environment, by default "dolphin-prod"
        if_exists : {'append', 'fail', 'replace'}
            Behavior when the destination table exists. Value can be one of:
            ``'fail'``
                If table exists raise pandas_gbq.gbq.TableCreationError.
            ``'replace'``
                If table exists, drop it, recreate it, and insert data.
            ``'append'``
                If table exists, insert data. Create if does not exist., by 
                default "append"
        **kwargs: dict, optional
            Extra arguments (such as a google BigQuery connection object) to be 
            passed to pandas_gbq's to_gbq function
        """

        data.to_gbq(
            destination_table=table,
            project_id=project_bq,
            if_exists=if_exists,
            credentials=self.credentials_bq,
            **kwargs
        )

        return None

    def data_to_mysql(self):
        pass 

    def data_to_psql(self):
        pass