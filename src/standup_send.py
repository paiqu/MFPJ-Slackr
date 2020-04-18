'''
Route for standup_send
'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError
from data import getData


SEND = Blueprint('send', __name__)

@SEND.route('/standup/send', methods=['POST'])
def send():
    '''function for route of standup send'''
    store = request.get_json()
    token = store['token']
    channel_id = int(store['channel_id'])
    message = store['message']

    return dumps(standup_send(token, channel_id, message))

def standup_send(token, channel_id, message):
    '''
    Input Error:
        channel_id is not valid
        message is more than 1000 characters
        An active standup is not currently running in this channel

    Access  Error:

    ASSUME: the token id is valid
    '''
    if channel_id_check(channel_id) == False:
        raise InputError("Invalid channel_id")
    if len(message) > 1000:
        raise InputError("Invalid message content")
    if channel_member_check(channel_id, token) == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")


    DATA = getData()
    standups = DATA['standups']
    channels = DATA['channels']
    users = DATA['users']

    for channel in channels:
        if channel['channel_id'] == channel_id:
            if channel['is_standup_active'] == False:
                raise InputError("Standup is not running in this channel")

    for user in users:
        if user['u_id'] == token_to_uid(token):
            user_name = user['name_first']
        for channel in channels:
            if channel['channel_id'] == channel_id:
                for standup in standups:
                    if standup['channel_id'] == channel_id:
                        message_list = f"{user_name}: {message}"
                        standup['messages'].append(message_list)
    return {}

