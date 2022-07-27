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
logging.basicConfig(level=logging.INFO)
# xray_recorder.configure(service='observability-app')
# XRayMiddleware(app, xray_recorder)


endpoints = ("one", "two", "three", "four", "five", "error")


@app.route("/one")
def first_route():
    time.sleep(random.random() * 0.2)
    logging.info('One endpoint request')
    return "ok"


@app.route("/two")
def the_second():
    time.sleep(random.random() * 0.4)
    logging.info('Two endpoint request')
    return "ok"


@app.route("/three")
def test_3rd():
    time.sleep(random.random() * 0.6)
    logging.info('Three endpoint request')
    return "ok"


@app.route("/four")
def fourth_one():
    time.sleep(random.random() * 0.8)
    logging.info('Four endpoint request')
    return "ok"

@app.route("/cats")
def cats_facts():
    random_number = random.randrange(0,10)
    
    if random_number > 6:
        try:
            r = requests.get('https://catfact.ninja/fact')
            response = r.json()
            logging.info('Getting cats information')
            return jsonify(response)
        except Exception as e:
            print(f"Error: {str(e)}")
            logging.error(f"{str(e)}")
            raise e
    try:    
        r = requests.get('https://catfact.nija/fact')
        print(r)
        return jsonify(r.json())
    except Exception as e:
        response = make_response(
                jsonify(
                    {"message": str(e)}
                ),
                503,
            )
        print(f"Error: {str(e)}")
        logging.error(f"{str(e)}")
        return response
   
@app.route("/error")
def oops():
    logging.error("Oops this is an injected error")
    return ":(", 500


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)

