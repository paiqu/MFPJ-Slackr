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
from flask import request, Flask, Blueprint, url_for, redirect
from json import dumps
from urllib.request import urlretrieve


PHOTO = Blueprint('/user/profile/uploadphoto', __name__)


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

    save_path = 'datas/' + str(token_to_uid(token)) + '.jpg'
    urllib.request.urlretrieve(img_url, "datas/website.jpg")
    buffer = Image.open("datas/website.jpg")
    area = (x_start, y_start, x_end, y_end)
    cropped_img = buffer.crop(area)
    cropped_img.save(save_path)

    new_url = 'http://localhost:5321/' + save_path
    print(new_url)
    
    DATA = getData()

    for user in DATA['users']:
        if user['u_id'] == token_to_uid(token):
            user['profile_img_url'] = new_url
    return {}
