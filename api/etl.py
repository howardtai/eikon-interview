import os
import pandas as pd
from sqlalchemy import types

# Constants
_DATA_PATH = "/app/data"

_TABLE_DTYPES = {
    "compound_id": types.BIGINT(),
    "compound_name": types.TEXT(),
    "compound_structure": types.TEXT(),
    "email": types.TEXT(),
    "experiment_compound_ids": types.ARRAY(types.BIGINT()),
    "experiment_count": types.BIGINT(),
    "experiment_id": types.BIGINT(),
    "experiment_run_time": types.BIGINT(),
    "name": types.TEXT(),
    "signup_date": types.DATE(),
    "user_id": types.BIGINT(),
    "usage_count": types.BIGINT(),
}

def save_dataframe_to_table(df, table_name, engine):
    df.to_sql(table_name, engine, if_exists="replace", index=False, dtype=_TABLE_DTYPES)


def load_data():
    # Load CSV files
    users = pd.read_csv(os.path.join(_DATA_PATH, "users.csv"), delimiter=r",\t")
    experiments = pd.read_csv(
        os.path.join(_DATA_PATH, "user_experiments.csv"), delimiter=r",\t"
    )
    compounds = pd.read_csv(os.path.join(_DATA_PATH, "compounds.csv"), delimiter=r",\t")

    # Format experiment table to have experiment_compound_ids as lists
    experiments["experiment_compound_ids"] = experiments[
        "experiment_compound_ids"
    ].str.split(";")

    # Format user table to have signup_date as datetime
    users["signup_date"] = pd.to_datetime(
        users["signup_date"], format="%Y-%m-%d"
    ).dt.normalize()

    return users, experiments, compounds


def create_user_compound_table(experiments):
    # Create user_compound table.
    exploded_experiments = experiments.explode(
        "experiment_compound_ids", ignore_index=True
    )
    exploded_experiments.rename(
        columns={"experiment_compound_ids": "compound_id"}, inplace=True
    )
    user_compound = (
        exploded_experiments.groupby(["user_id", "compound_id"])
        .size()
        .reset_index(name="usage_count")
    )
    return user_compound


def add_experiment_count_to_users_table(users, experiments):
    # Add total experiments to users table.
    total_experiments_per_user = experiments.groupby("user_id").size()
    total_experiments_per_user.rename("experiment_count", inplace=True)
    users = users.merge(
        total_experiments_per_user, left_on="user_id", right_on="user_id", how="left"
    )
    users["experiment_count"] = users["experiment_count"].fillna(0)
    return users


def process_etl(engine):
    users, experiments, compounds = load_data()

    users = add_experiment_count_to_users_table(users, experiments)
    user_compound = create_user_compound_table(experiments)

    # Upload data into PostgreSQL database
    save_dataframe_to_table(users, "users", engine)
    save_dataframe_to_table(experiments, "experiments", engine)
    save_dataframe_to_table(compounds, "compounds", engine)
    save_dataframe_to_table(user_compound, "user_compound", engine)
