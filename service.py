from flask import Flask, redirect, url_for, request
import flask
import os
import urllib.request
import requests
import json
import io
from base64 import encodebytes
from PIL import Image

app = Flask(__name__)


@app.route('/saveSet/<set>')
def save_set(set):
    os.mkdir(set)

    response = requests.get(f'https://api.scryfall.com/sets/{set}')
    search_uri = json.loads(response.text)['search_uri']

    response = requests.get(search_uri)
    cards = json.loads(response.text)['data']

    for card in cards:
        image_url = card['image_uris']['normal']
        urllib.request.urlretrieve(image_url, f'{set}/{card["name"]}.jpg')

    response = flask.jsonify({'success': True})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/loadSet/<set>')
def load_set(set):
    encoded_imges = []
    for file in os.listdir(f'{set}'):
        encoded_imges.append(get_response_image(file))


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode='r')
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
    return encoded_img


@app.route('/setExists/<set>')
def set_exists(set):
    response = flask.jsonify({'exists': os.path.exists(set)})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



if __name__ == '__main__':
    # encoded_imges = []
    # for file in os.listdir('dsc'):
    #     encoded_imges.append(get_response_image(file))
    #
    # print(encoded_imges)

    app.run(debug=True)
