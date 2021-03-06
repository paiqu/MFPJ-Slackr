'''
Can the only owner be removed?
FIX THIS LATER
'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, token_to_uid
from error import InputError, AccessError
from data import getData

RMVOWNER = Blueprint('channel_removeowner', __name__)

@RMVOWNER.route('/channel/removeowner', methods=['POST'])
def addowner():
    '''function for route channle/removeowner'''
    info = request.get_json()
    token = info['token']
    channel_id = int(info['channel_id'])
    u_id = int(info['u_id'])

    return dumps(channel_removeowner(token, channel_id, u_id))

def channel_removeowner(token, channel_id, u_id):
    '''function to remove an owner from a channel'''
    if not channel_id_check(channel_id):
        raise InputError("Channel ID is not a valid channel")

    DATA = getData()
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

    if target_user not in owners:
        raise InputError("user with user id u_id is not an owner of the channel")

    owners.remove(target_user)

    return {}
