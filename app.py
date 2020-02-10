from flask import Flask, jsonify
from flask_cors import CORS
from flask import render_template
import urllib.request, json

with urllib.request.urlopen("https://api-v3.mbta.com/predictions?filter[stop]=South+Station") as url:
    data = json.loads(url.read().decode())

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/', methods=['GET'])
def main_index():
    return jsonify(data)
    # return render_template('index.html');


@app.route('/southstation', methods=['Get'])
def south_station_arrivals():
    train_arrival = {}
    data_list = []
    for item in data["data"]:
        if item['attributes']['departure_time'] is not None:
            data_list.append({"train": {"status": item['attributes']['status'],
                                        "departure time": item['attributes']['departure_time'],
                                        "id": item['relationships']['route']['data']['id']}})
        # "arrival": item['arrival_time'],
        # if item['attributes']['arrival_time'] is not None:
        #     train_arrival = {'arrival_time': item['attributes']['arrival_time'],
        #                      'status': item['attributes']['status']}
    return jsonify(data_list)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/INSTAMATIC/<string:test_this_thing>')
def dappa_pong(test_this_thing):
    input_test = test_this_thing
    return input_test


if __name__ == '__main__':
    app.run()
