'''
Route for user setemail
'''
from json import dumps
from flask import Blueprint, request
from check_functions import check_email, token_to_uid
from error import InputError
from data import getData

SETEMAIL = Blueprint('setemail', __name__)

@SETEMAIL.route('/user/profile/setemail', methods=['PUT'])
def setemail():
    '''function for route of user setemail'''
    store = request.get_json()
    token = store['token']
    email = store['email']

    return dumps(user_setemail(token, email))

def user_setemail(token, email):
    '''
    Input Error:
        email is not valid
        email has been used by another user

    ASSUME: the token id is valid
    '''
    DATA = getData()
    if check_email(email) == False:
        raise InputError("Invalid email")
    for user in DATA['users']:
        if user['email'] == email:
            raise InputError("Email has been used by another user")

    for user in DATA['users']:
        if user['u_id'] == token_to_uid(token):
            user['email'] = email
    return {}

