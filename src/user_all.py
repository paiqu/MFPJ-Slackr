from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid
from error import InputError, AccessError

from class_file import User
from data import *

ALL = Blueprint('user_all', __name__)

@ALL.route('/user/all', methods=['GET'])
def list():
    token = request.form.get('token')
    return dumps(user_all(token, u_id))   

def user_all(token, u_id):
    '''
    Given a token, list all users associated with information 
    
    '''
    new_list = []
    
    global DATA
    DATA = getData()
    
    for user in DATA['users']:
        if user.u_id == token_to_uid
            new_dict = {}
            new_dict['u_id'] = user.u_id
            new_dict['name_first'] = user.name_first
            new_dict['name_last'] = user.name_last
            new_dict['email'] = user.email
            new_dict['handle'] = user.handle
            new_list.append(new_dict)
            
    return_dict['users'] = new_list
    return return_dict

