'''Route implementation for user/profile'''
from json import dumps
from flask import Blueprint, request
from error import InputError
from data import DATA, getData

PROFILE = Blueprint('profile', __name__)

@PROFILE.route('/user/profile', methods=['GET'])

def request_get():
    '''function for route user/profile'''
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    return user_profile(token, u_id)

def user_profile(token, u_id):
    '''
    For a valid user, returns information about their user id, email, 
    first name, last name, and handle
    '''
    
    DATA = getData()
    is_exist = False
    
    # check Input Error (User with u_id is not a valid user)
    for user in DATA['users']
        if user['u_id'] = u_id
            is_exist = True
    if not is_exist:
        raise InputError("Invalid u_id")
    
    # get user profile
    user = {'user':{}}
    for existuser in DATA['users']:
        if existuser['u_id'] == u_id:
            user['user']['u_id'] = existuser['u_id']
            user['user']['email'] = existuser['email']
            user['user']['name_first'] = existuser['name_first']
            user['user']['name_last'] = existuser['name_last']
            user['user']['handle_str'] = existuser['handle']
            
    return user
    
    
