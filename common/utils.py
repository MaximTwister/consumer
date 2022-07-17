from datetime import datetime

from database.models import (
    Model,
    Metric,
    MetricValues,
    Units,
)

# {
#  'timestamp': 1657955689,
#  'metric': {
#      'name': 'cpu_time_system',
#      'value': 108201.93,
#      'units': 'seconds'
#      },
#  'meta': {
#      'source_name': 'test-agent',
#      'hostname': 'Maxims-Air-M1',
#      'host_id': '8704af4b-7bec-4fa5-a514-17d03c6e631b'
#      }
# }


def save_data(data: dict):
    metric: dict = data.get("metric")
    meta: dict = data.get("meta")
    ts: str = data.get("timestamp")

    host_id = meta.get("host_id")

    metric_name = metric.get("name")
    metric_value = metric.get("value")
    units_name = metric.get("units")

    units_obj = is_units_exists(units_name)
    if not units_obj:
        units_obj = Units(name=units_name).save()

    model_obj = is_model_exists(host_id)
    if not model_obj:
        model_obj = Model(**meta).save()
    print(f"model: {model_obj}")

    metric_obj = is_metric_exists(metric_name, model_obj)
    if not metric_obj:
        metric_obj = Metric(name=metric_name, units=units_obj, model=model_obj).save()
    print(f"metric: {metric_obj}")

    if metric_obj not in model_obj.metrics:
        model_obj.metrics.append(metric_obj)
        model_obj.save()

    date_obj = datetime.fromtimestamp(int(ts))
    metric_value_obj = MetricValues(ts=date_obj, value=metric_value).save()
    metric_obj.values.append(metric_value_obj)
    metric_obj.save()
    print(f"metric was saved: {metric_obj}")


def is_metric_exists(metric_name, model):
    metric = None
    query = {"name": metric_name, "model": model}

    try:
        metric = Metric.objects.get(**query)
        print(f"[info] metric already exists")
    except Exception as e:
        print(f"[err] exception: {e} - {type(e)} - query: {query}")

    return metric


def is_model_exists(host_id):
    model = None

    try:
        model = Model.objects.get(host_id=host_id)
        print(f"[info] model already exists")
    except Exception as e:
        print(f"[err] exception: {e} - {type(e)}")

    return model


def is_units_exists(units_name):
    units = None

    try:
        units = Units.objects.get(name=units_name)
        print(f"[info] units already exists")
    except Exception as e:
        print(f"[err] exception: {e} - {type(e)}")

    return units
