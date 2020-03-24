from json import dumps
from flask import Blueprint, request
from check_error import token_check, check_email
from error import InputError, AccessError
from check_functions import token_to_uid

from class_file import User
from data import *

SETEMAIL = Blueprint('setemail', __name__)

@SETEMAIL.route('/setemail', methods=['PUT'])
def setemail():
    
    token = request.form.get('token')
    email = request.form.get('email')

    return dumps(user_setemail(token, email))

def user_setemail(token, email):
    '''
    Input Error:
        email is not valid
        email has been used by another user

    ASSUME: the token id is valid
    '''  
        
    if check_email == False:
        raise InputError("Invalid email")
    for user in DATA['users']:
        if user.email == email:
            raise InputError("Email has been used by another user")
    global DATA
    DATA = getData()
    
    for user in DATA['users']:
        if user.u_id == token_to_uid(token):
            user.email == email
    return {}