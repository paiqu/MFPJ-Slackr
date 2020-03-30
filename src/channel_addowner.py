from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, token_to_uid
from error import InputError, AccessError
from class_file import User
from data import DATA, getData

ADDOWNER = Blueprint('channel_addowner', __name__)

@ADDOWNER.route('/channel/addowner', methods=['POST'])
def addowner():
    '''function for route channle/addowner'''
    info = request.get_json()
    token = info['token']
    channel_id = int(info['channel_id'])
    u_id = int(info['u_id'])

    return dumps(channel_addowner(token, channel_id, u_id))

def channel_addowner(token, channel_id, u_id):
    if not channel_id_check(channel_id):
        raise InputError("Channel ID is not a valid channel")

    global DATA
    users = DATA['users']
    channels = DATA['channels']
    
    for user in users:
        if user['u_id'] == token_to_uid(token):
            function_caller = user
        
        if user['u_id'] == u_id:
            target_user = user
    
    for channel in channels:
        if channel['channel_id'] == channel_id:
            target_channel = channel

    owners = target_channel['owners']

    if function_caller not in owners and not function_caller['is_slack_owner']:
        raise AccessError("the authorised user is not an owner of the slackr, or an owner of this channel")


    if target_user in owners:
        raise InputError('User with u_id is already an owner of the channel')

    
    owners.append(target_user)

    return {}
    