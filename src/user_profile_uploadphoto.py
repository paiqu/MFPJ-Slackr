from check_functions import token_to_uid
from error import InputError
from data import getData
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL
import os
from PIL import Image
import webbrowser
from urllib.request import urlopen


PHOTO = Blueprint('/user/profile/uploadphoto', __name__)

app = Flask(__name__)
app.config['UPLOADED_PHOTO_DEST'] = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES

def dest(name):
    return '{}/{}'.format(UPLOAD_DEFAULT_DEST, name)
#app.config['UPLOAD_PHOTO_URL'] = 'http://localhost:5321/'
photos = UploadSet('PHOTO')

configure_uploads(app, photos)

# Example
APP.config['UPLOADED_PHOTO_DEST'] = os.path.dirname(os.path.abspath(__file__))
APP.config['UPLOADED_PHOTO_ALLOW'] = IMAGES
def dest(name):
    return '{}/{}'.format(UPLOAD_DEFAULT_DEST, name)
#app.config['UPLOAD_PHOTO_URL'] = 'http://localhost:5321/'
photos = UploadSet('PHOTO')

configure_uploads(APP, photos)

@APP.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        rec = Photo(filename=filename, user=g.user.id)
        rec.store()
        flash("Photo saved.")
        return redirect(url_for('show', id=rec.id))
    return render_template('upload.html')

@APP.route('/photo/<id>')
def show(id):
    photo = Photo.load(id)
    if photo is None:
        abort(404)
    url = photos.url(photo.filename)
    return render_template('show.html', url=url, photo=photo)

@APP.route('/user/profile/uploadphoto', methods=['POST'])
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

    DATA = getData()

    for user in DATA['users']:
        if user['u_id'] == token_to_uid(token):
            user['img_url'] = img_url
            break
    
    img = Image.open(urlopen(img_url))

    area = (x_start, y_start, x_end, y_end)
    cropped_img = img.crop(area)
    cropped_img.show()

    return {}