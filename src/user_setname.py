from json import dumps
from flask import Blueprint, request
from check_error import token_check
from error import InputError, AccessError
from check_functions import token_to_uid

from class_file import User
from data import *

SETNAME = Blueprint('setname', __name__)

@SETNAME.route('/setname', methods=['PUT'])
def setname():
    
    token = request.form.get('token')
    name_first = request.form.get('name_first')
    name_last = request.form.get('name_last')

    return dumps(user_setname(token, name_first, name_last))

def user_setname(token, name_first, name_last):
    '''
    Input Error:
        name_first is not between 1 and 50 characters inclusive in length
        name_last is not between 1 and 50 characters inclusive in length
    
    ASSUME: the token id is valid
    '''
    if name_first < 1 or name_first > 50 or name_last < 1 or name_last > 50
        raise InputError("Invalid first name and last name")

    global DATA
    DATA = getData()
    
    for user in DATA['users']:
        if user.u_id == token_to_uid(token):
            user.name_first == name_first
            user.name_last == name_last
    return {}


