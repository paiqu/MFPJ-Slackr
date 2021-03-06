'''
Route for user sethandle
'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid
from error import InputError
from data import getData

SETHANDLE = Blueprint('sethandle', __name__)

@SETHANDLE.route('/user/profile/sethandle', methods=['PUT'])
def sethandle():
    '''function for route of user sethandle'''
    store = request.get_json()
    token = store['token']
    handle_str = store['handle_str']

    return dumps(user_sethandle(token, handle_str))

def user_sethandle(token, handle_str):
    '''
    Input Error:
        handle is not between 2 and 20 characters
        handle has been used by another user

    ASSUME: the token id is valid
    '''
    DATA = getData()
    if  len(handle_str) < 2 or len(handle_str) > 20:
        raise InputError("Invalid handle")
    for user in DATA['users']:
        if user['handle'] == handle_str:
            raise InputError("Handle has been used")

    for user in DATA['users']:
        if user['u_id'] == token_to_uid(token):
            user['handle'] = handle_str
    return {}
