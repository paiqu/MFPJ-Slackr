'''Route implementation for user/profile'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid
from error import InputError
from class_file import User
from data import DATA, getData

PROFILE = Blueprint('profile', __name__)

@PROFILE.route('/profile', methods=['Get'])

def request_get():
    '''function for route user/profile'''
    token = request.form.get('token')
    u_id = request.form.get('u_id')
    return dumps(user_profile(token, u_id))

def user_profile(token, u_id):
    '''
    For a valid user, returns information about their user id, email, 
    first name, last name, and handle

    Input Error:
        invlid channel_id
    
    ASSUME: the token id is valid
    '''
    user_id = token_to_uid(token)
    if user_id != u_id:
        raise InputError("Invalid u_id")

    global DATA
    DATA = getData()
    
    user = {}
    
    for existuser in DATA['users']:
        if existuser.u_id == user_id:
            user['u_id'] = existuser.u_id
            user['email'] = existuser.email
            user['name_first'] = existuser.name_first
            user['name_last'] = existuser.name_last
            user['handle_str'] = existuser.handle
            
    return {user}



       

