'''Route implementation for auth/passwordreset/request'''
from json import dumps
from flask import Blueprint, request
from check_functions import user_exists_check
from class_file import User
from data import DATA, getData
from flask_mail import Mail
import random
import string

PASSWORDRESET_REQUEST = Blueprint('passwordreset_request', __name__)



@PASSWORDRESET_REQUEST.route('/auth/passwordreset/request', methods=['POST'])
def reset_request():
    '''function for route passwordreset/request'''
    info = request.get_json()
    email = info['email']
    return dumps(passwordreset_request(email))


def passwordreset_request(email):
    '''
    Given an email address, if the user is a registered user,
    send's them a an email containing a specific secret code
    '''
    if user_exists_check(email):
        secret_code = ''.join(random.choice(string.digits) for _ in range(5))
        msg = Message(secret_code,
                      recipients=[email])
        mail.send(msg)
        DATA = getData()
        for user in DATA['users']:
            if user['email'] == email:
                user['reset_code'] = secret_code

    return {}
