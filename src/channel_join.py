from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, token_to_uid
from error import InputError, AccessError
from class_file import User
from data import DATA, getData

JOIN = Blueprint('channel_join', __name__)

@JOIN.route('/channel/join', methods=['POST'])
def join():
    '''function for route channle/join'''
    info = request.get_json()
    token = info['token']
    channel_id = int(info['channel_id'])

    return dumps(channel_join(token, channel_id))

def channel_join(token, channel_id):
    '''
    token -- String
    channel_id -- Int
    '''

    if not channel_id_check(channel_id):
        raise InputError("Channel ID is not a valid channel")
    

    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']

    for user in users:
        if user['u_id'] == token_to_uid(token):
            target_user = user

    for channel in channels:
        if channel['channel_id'] == channel_id:
            target_channel = channel
    
    owners = target_channel['owners']

    if target_user in target_channel['members']:
        raise AccessError("The user is already a memeber in this channel")
    
    if (not target_user['is_slack_owner']) and (target_user not in owners) and (not target_channel['is_public']):
        raise AccessError("A user who is not a owner of channel or owner of slackr cannot join a private channel")

    members = target_channel['members']
    members.append(target_user)

    return {}

