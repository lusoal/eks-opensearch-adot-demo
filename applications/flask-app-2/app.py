import time
import random
import requests

from flask import Flask, jsonify, make_response
from prometheus_flask_exporter import PrometheusMetrics
# from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.ext.flask.middleware import XRayMiddleware


app = Flask(__name__)
PrometheusMetrics(app)
# xray_recorder.configure(service='observability-app')
# XRayMiddleware(app, xray_recorder)


endpoints = ("service_1", "error")


@app.route("/service_1")
def first_route():
    r = requests.get('http://observability-app.observability-app.svc.cluster.local/one')
    response = str(r.text)
    return jsonify({"message":response})

 
@app.route("/error")
def oops():
    return ":(", 500


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)