import time
import random
import requests
import logging

from flask import Flask, jsonify, make_response
from prometheus_flask_exporter import PrometheusMetrics
# from aws_xray_sdk.core import xray_recorder
# from aws_xray_sdk.ext.flask.middleware import XRayMiddleware


app = Flask(__name__)
PrometheusMetrics(app)
FORMAT = 'log: {' + ' %(asctime)s %(levelname)s:%(message)s}'
logging.basicConfig(level=logging.INFO, format=FORMAT)
# xray_recorder.configure(service='observability-app')
# XRayMiddleware(app, xray_recorder)


endpoints = ("service_1", "error")

def log_json_parser(log_message, kind): 
    if "error" in kind:
        logging.error(log_message)
    else:
        logging.info(log_message)
    

@app.route("/service_1")
def first_route():
    r = requests.get('http://flask-app-1.flask-app-1.svc.cluster.local/one')
    response = str(r.text)
    
    log_message = 'Request for flask-app-1'
    log_json_parser(log_message, "info")
    
    return jsonify({"message":response})

 
@app.route("/error")
def oops():
    log_message = "Oops this is an injected error"
    log_json_parser(log_message, "error")
    return ":(", 500


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)