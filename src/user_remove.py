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
    token = request.args.get('login_token')
    u_id = int(request.args.get('u_id'))
    #u_id = int(u_id)

    #info = request.get_json()
    #info = request.args.get()
    #token = info['login_token']
    #u_id= int(info['u_id'])

    return dumps(remove_user(token, u_id))

def remove_user(token, u_id):
    '''
    Removes user from slackr 
    Removes them from all of the channels they belong to - owners and members
    '''

    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']

    # Checks the User ID is valid
    if user_id_check(u_id) == False:
        raise InputError("This is not a valid user or user ID")

    for user in users:
        if user['u_id'] == token_to_uid(token):
            admin_user = user
    for user in users:
        if user['u_id'] == u_id:
            sub_user = user         

    

    # If not slackr owner
    if admin_user['is_slack_owner'] == False:
        raise AccessError('This user is not a slackr owner')
  
    
    # Removes user as member of any channels 
    for channel in channels:
        for user in channel['members']:
            if user == sub_user:
                channel['members'].remove(user)
    
    # Removes user as owner of any channels
    for channel in channels:
        for user in channel['owners']:
            if user == sub_user:
                channel['owners'].remove(user)
    
    #Removes user for user database
    users.remove(sub_user)



    return {}

    


