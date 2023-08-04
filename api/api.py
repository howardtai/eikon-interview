from etl import process_etl
from flask import Flask, request

app = Flask(__name__)


@app.route("/trigger_etl", methods=["POST"])
def trigger_etl():
    process_etl()
    return {"message": "ETL process started"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
