'''Route implementation for channel/invite'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError
from token_functions import generateToken

from data import DATA, getData

INVITE = Blueprint('invite', __name__)

@INVITE.route('/channel/invite', methods=['POST'])
def invite():
    info = request.get_json()
    token = info['token']

    # Why do we need to cast _id to an int?
    channel_id = int(info['channel_id'])
    u_id = int(info['u_id'])

    return dumps(channel_invite(token, channel_id, u_id))



def channel_invite(token, channel_id, u_id):
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']

    ###Need to add a function for in case the user of token is not verified to invite other users 
    for user in users:
        if user['u_id'] == token_to_uid(token):
            target_user = user

    for channel in channels:
        if channel['channel_id'] == channel_id:
            target_channel = channel
    
    owners = target_channel['owners']

    if target_user in target_channel['members']:
        raise AccessError("The user is already a memeber in this channel")
    
    members = target_channel['members']
    members.append(target_user)

    return {}

