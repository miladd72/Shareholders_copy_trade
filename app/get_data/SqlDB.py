import pandas as pd
import pyodbc

from app.configs import SERVER, DATABASE, USERNAME, PASSWORD
from .sql_queries import *


class SQL:
    def __init__(self, **kwargs):
        server = kwargs.get("DB_SERVER", SERVER)
        database = kwargs.get("DB_PORT", DATABASE)
        username = kwargs.get("DB_USER", USERNAME)
        password = kwargs.get("DB_PASS", PASSWORD)

        self.conn_str = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'

    def get_data(self, table_name, columns=None, filters=None, limit=None, sort=None):
        query = f'SELECT {", ".join(columns) if columns else "*"} FROM {table_name}'

        if filters:
            filter_conditions = [f"{col} {op} {val}" for col, op, val in filters]
            query += f' WHERE {" AND ".join(filter_conditions)}'

        if sort:
            query += f' ORDER BY {", ".join(sort)}'

        if limit:
            query = f'SELECT TOP {limit} {", ".join(columns) if columns else "*"} FROM {table_name}'

            if filters:
                filter_conditions = [f"{col} {op} {val}" for col, op, val in filters]
                query += f' WHERE {" AND ".join(filter_conditions)}'

            if sort:
                query += f' ORDER BY {", ".join(sort)}'

        df = self.__send_query(query)

        return df

    def get_diff_shares_primary(self):
        query = primary_stocks_shareholders_change

        df = self.__send_query(query)

        return df

    def get_diff_shares_primary_with_feature(self):
        query = primary_stocks_shareholders_change_with_features

        df = self.__send_query(query)

        return df

    def __send_query(self, query):
        conn = pyodbc.connect(self.conn_str)
        try:
            df = pd.read_sql_query(query, conn).reset_index(drop=True)
        except Exception as e:
            print(f"Error executing SQL query: {str(e)}")
            df = pd.DataFrame()
        finally:
            conn.close()
        return df

if __name__ == "__main__":
    SQL().get_diff_shares_primary()
