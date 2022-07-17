import json

from flask import (
    Flask,
    jsonify,
    request,
    make_response,
)

from common.utils import save_data
from database.db import initialize_db

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
    "db": "consumer",
    "host": "mongodb+srv://twister:twister@cluster0.xwhmh.mongodb.net/consumer"
}

initialize_db(app)


@app.route("/api/v1/metrics", methods=["POST"])
def post_metrics():
    data: dict = json.loads(request.data)
    meta_field = data.get("meta")

    if not meta_field:
        response_data = {"err": "unprocessable entity - metric has no meta-data"}
        return make_response(jsonify(response_data), 422)

    save_data(data)

    print(f"received metric: {data}")
    response_data = {"message": "metric_consumed", "code": "SUCCESS"}
    return make_response(jsonify(response_data), 201)


if __name__ == "__main__":
    port = 5001
    app.run(debug=True, host="0.0.0.0", port=port)
