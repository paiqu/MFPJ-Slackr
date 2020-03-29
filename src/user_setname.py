from json import dumps
from flask import Blueprint, request
from check_functions import token_check, token_to_uid
from error import InputError

from class_file import User
from data import *
from workspace_reset import reset

SETNAME = Blueprint('setname', __name__)

@SETNAME.route('/user/setname', methods=['PUT'])
def setname():
    '''function for route of user setname'''
    store = request.get_json()
    token = store['token']
    name_first = store['name_first']
    name_last = store['name_last']

    return dumps(user_setname(token, name_first, name_last))

def user_setname(token, name_first, name_last):
    '''
    Input Error:
        name_first is not between 1 and 50 characters inclusive in length
        name_last is not between 1 and 50 characters inclusive in length
    
    ASSUME: the token id is valid
    '''
    if len(name_first) < 1 or len(name_first) > 50 or len(name_last) < 1 or len(name_last) > 50:
        raise InputError("Invalid first name and last name")

    DATA = getData()
    
    for user in DATA['users']:
        if user['u_id'] == token_to_uid(token):
            user['name_first'] == name_first
            user['name_last'] == name_last
    return {}