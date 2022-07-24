import json

from flask import (
    Flask,
    jsonify,
    request,
    make_response,
    render_template,
)

from common.utils import (
    save_data,
    load_models,
    load_metrics,
    get_metric_data,
)
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


@app.route("/api/v1/models", methods=["GET"])
def get_api_models():
    models = load_models()
    return make_response(jsonify(models), 201)


@app.route("/values/<host_id>/<metric_name>")
def get_metric_values(host_id, metric_name):
    values, units = get_metric_data(host_id, metric_name)


@app.route("/metrics/<host_id>", methods=["GET"])
def get_metrics(host_id):
    metrics = load_metrics(host_id)
    return make_response(jsonify(metrics), 201)


@app.route("/models", methods=["GET"])
def get_models():
    models = load_models()
    return render_template("models.html", models=models)


if __name__ == "__main__":
    port = 5001
    app.run(debug=True, host="0.0.0.0", port=port)
