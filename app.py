from flask_cors import CORS
import urllib.request, json
from flask import Flask, request, url_for, redirect, render_template

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/', methods=['GET'])
def main_index():
    return render_template('index2-pagefold.html')


@app.route('/item-1.html', methods=['GET', 'POST'])
def north_station_table():
    if request.method == 'POST':
        return redirect(url_for('item-1.html'))
    data = get_data("North+Station")
    data_list = build_table(data)
    return render_template('tabletemplate.html', posts=data_list)


@app.route('/item-2.html', methods=['GET', 'POST'])
def south_station_table():
    if request.method == 'POST':
        return redirect(url_for('item-2.html'))
    data = get_data("South+Station")
    data_list = build_table(data)
    return render_template('tabletemplate.html', posts=data_list)


# Filters data and Builds table for each station
def build_table(data):
    data_list = []
    for item in data["data"]:
        if item['attributes']['departure_time'] is not None:
            train_info = {"train": {"status": item['attributes']['status'],
                                    "departure_time": item['attributes']['departure_time'][12:16],
                                    "id": item['relationships']['route']['data']['id']}}
            data_list.append(train_info)
    return data_list


# Fetches data from api
def get_data(station_name):
    url_string = "https://api-v3.mbta.com/predictions?filter[stop]=" + station_name
    with urllib.request.urlopen(url_string) as url:
        data = json.loads(url.read().decode())
    return data


if __name__ == '__main__':
    app.run()
