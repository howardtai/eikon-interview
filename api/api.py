import pandas as pd
from flask import Flask, jsonify
from sqlalchemy import create_engine, exc

from etl import process_etl

# Db constants
_DB_NAME = "db_name"
_DB_USER = "db_user"
_DB_PWD = "db_password"
_DB_HOST = "db"  # name of the db container
_DB_PORT = 5432  # postgresql default port

app = Flask(__name__)


def create_postgresql_engine(user, pwd, host, port, database):
    try:
        url = f"postgresql://{user}:{pwd}@{host}:{port}/{database}"
        engine = create_engine(url)
        return engine
    except exc.SQLAlchemyError as e:
        print("Error creating the database engine:", e)
        return None


engine = create_postgresql_engine(_DB_USER, _DB_PWD, _DB_HOST, _DB_PORT, _DB_NAME)


@app.route("/trigger_etl", methods=["POST"])
def trigger_etl():
    process_etl(engine)
    return {"message": "ETL process started"}, 200


@app.route("/total_experiments", methods=["GET"])
def total_experiments():
    query = "SELECT user_id, experiment_count as total_experiments FROM users;"
    results = pd.read_sql(query, con=engine)
    return jsonify(results.to_dict(orient="records"))


@app.route("/average_experiments", methods=["GET"])
def average_experiments():
    query = "SELECT AVG(experiment_count) as average_experiments FROM users;"
    results = pd.read_sql(query, con=engine)
    return jsonify(results.to_dict(orient="records"))


@app.route("/most_common_compound", methods=["GET"])
def most_common_compound():
    query = """
    SELECT compound_id, SUM(usage_count) as total_usage
    FROM user_compound
    GROUP BY compound_id
    ORDER BY total_usage DESC
    LIMIT 1;
    """
    results = pd.read_sql(query, con=engine)
    return jsonify(results.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
