'''
Route for user_all
'''
from json import dumps
from flask import Blueprint, request
from data import getData

ALL = Blueprint('users_all', __name__)

@ALL.route('/users/all', methods=['GET'])
def alluser():
    '''function for route of users all'''
    token = request.args.get('token')
    return dumps(users_all(token))

def users_all(token):
    '''
    Given a token, list all users associated with information
    '''
    DATA = getData()
    new_list = []
    for user in DATA['users']:
        new_dict = {}
        new_dict['u_id'] = user['u_id']
        new_dict['email'] = user['email']
        new_dict['name_first'] = user['name_first']
        new_dict['name_last'] = user['name_last']
        new_dict['handle'] = user['handle']
        new_dict['profile_img_url'] = user['profile_img_url']
        new_list.append(new_dict)
    return_dict = {}
    return_dict['users'] = new_list
    return return_dict
