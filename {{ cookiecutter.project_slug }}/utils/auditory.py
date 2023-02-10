import numpy as np
import pandas as pd

import json
import sys
import mysql.connector
from mysql.connector import Error


class Auditory:
    def __init__(self, path_credentials_mariaDB: str) -> None:
        """
        path_credentials_mariaDB: str. Path to json file with credentials for
        accest to rino replica database
        """

        self.path_cred_mariaDB = path_credentials_mariaDB
        with open(self.path_cred_mariaDB) as json_file:
            self.credentials_rino = json.load(json_file)
            json_file.close()
        self.conn_rino = self.connect_mariaDB(self.credentials_rino)
        self.cursor_rino = self.conn_rino.cursor()

    def connect_mariaDB(self, params_dic: dict):
        """
        params_dic: Dictionary with credentials values
        """

        """ Connect to the MariaDB database server """
        conn = None
        try:
            # connect to the MariaDB server (auditory)
            print("Connecting to the MariaDB database...")
            conn = mysql.connector.connect(**params_dic)
            if conn.is_connected():
                db_Info = conn.get_server_info()
                print("Connected to MarioDB Server version ", db_Info)
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
        except Error as e:
            print("Error while connecting to MarioDB", e)
            sys.exit(1)

        return conn

    def update_audit(
        self,
        start_date: int,
        start_time: int,
        end_date: int,
        end_time: int,
        process_number: str,
        data: int,
        verify_procces_executed: bool = True,
        obs1: str = "NULL",
        obs2: str = "NULL",
        obs3: str = "NULL",
        audit_database="develop",
    ) -> None:
        """
        audit_database: str ('develop', 'production').
            Database to save the auditory, default is develop
        obs1: Default is 'NULL'.
        obs2: Optional
        obs3: Optional
        """

        database = "audit_monitoring_dev"

        if audit_database not in ["develop", "production"]:
            raise ValueError("Trying to save audit on an unknown database")

        if audit_database == "production":
            database = "audit_monitoring"

        if data == 0:
            obs1 = "Sin registros en origen"

        # Check if proccess was executed and the number of processed data is
        # equal in the whole day
        if verify_procces_executed and data != 0:
            # Get last execution current date
            query = f""" 
                SELECT *
                FROM bi.{database} AS audit
                WHERE audit.id_process = {process_number}
                ORDER BY audit.start_date DESC;
            """

            self.cursor_rino.execute(query)
            columns = [
                "id_run",
                "id_process",
                "start_date",
                "start_time",
                "end_date",
                "end_time",
                "data",
                "obs1",
                "obs2",
                "obs3",
            ]
            df_executed = pd.DataFrame(self.cursor_rino.fetchall(), columns=columns)
            df_executed = df_executed.loc[df_executed.start_date == int(start_date)]
            df_executed.sort_values(
                by=["start_date", "start_time"], ascending=False, inplace=True
            )

            # ddddddddddddddddddd
            if len(df_executed) != 0:
                data_precessed = df_executed.data.sum()

                # Define if process was or not executed
                if ((data_precessed == data) or (np.isnan(data_precessed))) and (
                    data_precessed != 0
                ):
                    data = "NULL"
                    obs1 = "Proceso ya ejecutado"
                else:
                    data = abs(data_precessed - data)

        # Set observations
        def set_observation(obs):
            if obs != "NULL":
                obs = f"'{obs}'"
            return obs

        obs1, obs2, obs3 = (set_observation(obs) for obs in [obs1, obs2, obs3])

        # Query
        query = f""" 
        INSERT INTO {database}
            (id_process,
            start_date,
            start_time,
            end_date,
            end_time,
            `data`,
            obs1,
            obs2,
            obs3
            )
        VALUES ({process_number},
                {start_date},
                {start_time},
                {end_date},
                {end_time},
                {data},
                {obs1},
                {obs2},
                {obs3}		
                );
        """
        self.cursor_rino.execute(query)
        self.conn_rino.commit()
        print(self.cursor_rino.rowcount, "Record inserted successfully")
