'''
Route implementation for admin/user/remove

Given a User by their user ID, remove the user from the slackr.
'''

from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid, user_id_check
from channels_list import channels_list
from channel_addowner import channel_addowner
from error import InputError, AccessError
from token_functions import generate_token
from class_file import User, Channel
from data import DATA, getData

RMVUSER = Blueprint('remove_user', __name__)


@RMVUSER.route('/admin/user/remove', methods=['DELETE'])

def rmv_user():
    '''
    request info for remove user
    '''

    info = request.get_json()
    token = info['token']
    u_id= int(info['u_id'])

    return dumps(remove_user(token, u_id))

def remove_user(token, u_id):
    '''
    Removes user from slackr 
    Removes them from all of the channels they belong to 
    '''

    authorised_user = token_to_uid(token)

    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']

    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']

    for user in users:
        if user['u_id'] == token_to_uid(token):
            admin_user = user
    for user in users:
        if user['u_id'] == u_id:
            sub_user = user         

    # Checks the User ID is valid
    if user_id_check(u_id) == False:
        raise InputError("This is not a valid user or user ID")


    # If the wrong permission ID is entered 
    if permission_id != 1:
        raise InputError('This is not a valid permission number')

    # The admin user has permission priviledges 
    if admin_user['global_permission'] != 1:
        raise AccessError("The admin user is not authorised")
    
    #changes the sub users permission having passed all checks 

    #### IS THIS RIGHT?
    sub_user['global_permission'] = permission_id
    

    #changes the users permission privileges to owner if they aren't already owner 
    for channel in channels_list(sub_user['token'])['channels']:
        if sub_user not in channel['owners']:
            
            channel_addowner(admin_user['token'], channel['channel_id'], sub_user['u_id'])

    return {}

    


