from .absolute_paths import AbsPaths

from google.oauth2 import service_account


class MakeConnection(AbsPaths):
    """
    Class to make connections with different types of RDBMS (MySQL, Postgres, 
    BigQuery, etc)

    Attributes
    ----------
    max_level: int
        Maximum level of depth within the package, in which it seeks to establish
        the absolute paths. Inherited from the AbsPaths class
    file_credentials_path: str
        Absolute path to the .json credentials file to BigQuery. Only if the
        with_gbq() method is used
    credentials_bq: service_account
        Connection object to BigQuery using a service account. Only if the
        with_gbq() method is used

    """

    def __init__(self, max_level: int = 5) -> None:
        """
        Parameters
        ----------
        max_level : int, optional
            Maximum level of depth to perform the construction of routes in the
            package, by default 5.

            This is done using the methods of the AbsPath class which allows
            handling paths within the package.
        """

        super().__init__(max_level=max_level)

    def with_gqb(
        self,
        file_credentials_path: str = None,
        file_credentials_name: str = "credentials_bq.json",
    ) -> None:
        """
        Connect to a BigQuery database.

        Parameters
        ----------
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

        """

        self.file_credentials_path = file_credentials_path

        if file_credentials_path is None:
            self.file_credentials_path = self.get_abs_path_file(file_credentials_name)

        self.credentials_bq = service_account.Credentials.from_service_account_file(
            self.file_credentials_path
        )

        return None
