import pandas as pd
import os
import psycopg2
from sqlalchemy import create_engine

_DATA_PATH = "/app/data"
_DB_NAME = "db_name"
_DB_USER = "db_user"
_DB_PWD = "db_password"
_DB_HOST = "db"  # name of the db container
_DB_PORT = 5432  # postgresql default port


def process_etl():
    # Load CSV files
    users = pd.read_csv(os.path.join(_DATA_PATH, "users.csv"), delimiter=r",\t")
    experiments = pd.read_csv(
        os.path.join(_DATA_PATH, "user_experiments.csv"), delimiter=r",\t"
    )
    compounds = pd.read_csv(os.path.join(_DATA_PATH, "compounds.csv"), delimiter=r",\t")

    # TODO: Process files to derive features

    # Upload data into PostgreSQL database
    engine = create_engine(
        url="postgresql://{user}:{pwd}@{host}:{port}/{database}".format(
            user=_DB_USER, pwd=_DB_PWD, host=_DB_HOST, port=_DB_PORT, database=_DB_NAME
        )
    )
    users.to_sql("users", engine, if_exists="replace")
    experiments.to_sql("experiments", engine, if_exists="replace")
    compounds.to_sql("compounds", engine, if_exists="replace")
