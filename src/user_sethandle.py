from json import dumps
from flask import Blueprint, request
from check_error import token_check
from error import InputError, AccessError
from check_functions import token_to_uid

from class_file import User
from data import *

SETHANDLE = Blueprint('sethandle', __name__)

@SETHANDLE.route('/sethandle', methods=['PUT'])
def sethandle():
    store = request.get_json()
    token = store['token']
    handle = store['handle']

    return dumps(user_sethandle(token, handle))

def user_sethandle(token, handle):
    '''
    Input Error:
        handle is not between 2 and 20 characters
        handle has been used by another user

    ASSUME: the token id is valid
    '''  
        
    if  handle < 2 or handle > 20:
        raise InputError("Invalid handle")
    for user in DATA['users']:
        if user.handle == handle:
            raise InputError("Handle has been used")
    global DATA
    DATA = getData()
    
    for user in DATA['users']:
        if user.u_id == token_to_uid(token):
            user.handle == handle
    return {}