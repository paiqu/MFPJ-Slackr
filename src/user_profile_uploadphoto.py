from check_functions import token_to_uid
from error import InputError
from data import getData
import os
from PIL import Image
import webbrowser
import urllib.request
import urllib
import re
import requests
from io import StringIO
from flask import Blueprint, request, send_file
from json import dumps

PHOTO = Blueprint('/user/profile/uploadphoto', __name__)
UPLOAD = Blueprint('/croppedimage', __name__)

@PHOTO.route('/user/profile/uploadphoto', methods=['POST'])
def setphoto():

    store = request.get_json()
    token = store['token']
    img_url = str(store['img_url'])
    x_start = int(store['x_start'])
    y_start = int(store['y_start'])
    x_end = int(store['x_end'])
    y_end = int(store['y_end'])
    return dumps(user_setphoto(token, img_url, x_start, y_start, x_end, y_end))


def user_setphoto(token, img_url, x_start, y_start, x_end, y_end):

    img_data = requests.get(img_url).content
    with open('website.jpg','wb') as picture:
        picture.write(img_data)

    area = (x_start, y_start, x_end, y_end)
    imagelocal = Image.open('website.jpg')
    cropped_img = imagelocal.crop(area)

    cropped_img.save("croppedimage.jpg")

    img()
    new_url = 'http://localhost:1239/croppedimage'

    print(new_url)
    DATA = getData()

    for user in DATA['users']:
        if user['u_id'] == token_to_uid(token):
            user['img_url'] = new_url

    return {}

@UPLOAD.route("/croppedimage")
def img():
    return send_file('./croppedimage.jpg', mimetype='image/jpg')
    