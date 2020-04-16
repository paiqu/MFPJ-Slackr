from check_functions import token_to_uid
from error import InputError
from data import getData
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL
import os
from PIL import Image
import webbrowser
import urllib.request
import urllib
import re
import requests
from StringIO import StringIO


PHOTO = Blueprint('/user/profile/uploadphoto', __name__)

@PHOTO.route('/user/profile/uploadphoto', methods=['POST'])
def setphoto():

    store = request.get_json()
    token = store['token']
    img_url = store['img_url']
    x_start = store['x_start']
    y_start = store['y_start']
    x_end = store['x_end']
    y_end = store['y_end']
    return dumps(user_setphoto(token, img_url, x_start, y_start, x_end, y_end))


def user_setphoto(token, img_url, x_start, y_start, x_end, y_end):

    r = requests.get(img_url)

    img = Image.open(StringIO(r.content))
    img.save('website.jpg')

    area = (x_start, y_start, x_end, y_end)

    cropped_img = img.crop(area)
    cropped_img.save('import/glass/5/z5237481/uploads',format = 'JPEG')

    new_url = 'http://0.0.0.0:5321/' + '/import/glass/5/z5237481/uploads'

    '''
    img = Image.open(r)

    urllib.urlretrieve(img_url, "photos.jpg")
    '''

    
    DATA = getData()

    for user in DATA['users']:
        if user['u_id'] == token_to_uid(token):
            user['img_url'] = new_url

    return {}