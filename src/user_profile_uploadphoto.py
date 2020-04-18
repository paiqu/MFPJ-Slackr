'''
Route for user_profile_uploadphoto
'''
from json import dumps
from urllib.request import urlretrieve
from flask import request, Blueprint
from PIL import Image
import requests
from check_functions import token_to_uid
from error import InputError
from data import getData



PHOTO = Blueprint('/user/profile/uploadphoto', __name__)


@PHOTO.route('/user/profile/uploadphoto', methods=['POST'])
def setphoto():
    '''
    Setphoto
    '''
    store = request.get_json()
    token = store['token']
    img_url = str(store['img_url'])
    x_start = int(store['x_start'])
    y_start = int(store['y_start'])
    x_end = int(store['x_end'])
    y_end = int(store['y_end'])

    return dumps(user_setphoto(token, img_url, x_start, y_start, x_end, y_end))

def user_setphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''
    This function for the setphoto route
    '''
    form = "jpg"
    if form not in img_url:
        raise InputError("This image is not jpg format")

    r = requests.get(img_url)
    if r.status_code != 200:
        raise InputError("This image_url is invalid")
    u_id = str(token_to_uid(token))
    save_path = 'static/' + u_id + '.jpg'
    photo_name = f"./static/{u_id}.jpg"
    urlretrieve(img_url, photo_name)
    img = Image.open(photo_name)

    width, height = img.size

    if x_start > width or x_end > width or y_start > height or y_end > height:
        raise InputError("This crop image is out of range")
    if x_start < 0 or x_end < 0 or y_start < 0 or y_end < 0:
        raise InputError("This crop image is out of range")
    area = (x_start, y_start, x_end, y_end)
    cropped_img = img.crop(area)
    cropped_img.save(save_path)

    new_url = str(request.url_root) + save_path
    DATA = getData()
    print(new_url)
    for user in DATA['users']:
        if user['u_id'] == token_to_uid(token):
            user['profile_img_url'] = new_url

    return {}
