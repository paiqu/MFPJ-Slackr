'''Route implementation for message_unpin'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, channel_member_check, message_id_check
from error import InputError, AccessError
from data import DATA, getData

UNPIN = Blueprint('message_unpin', __name__)

@UNPIN.route('/message/unpin', methods=['POST'])
def request_get():
    '''request get for route message pin'''
    request = request.get_json()
    token = request['token']
    message_id = int(request['message_id'])
    message_unpin(token, message_id)
    return dumps({})

def message_unpin(token, message_id):
    ''' Given a message within a channel, remove it's mark as unpinned'''
    if not message_id_check(message_id):
        raise InputError("message_id is not a valid message")

    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    messages = DATA['messages']

    for message in messages:
        if message['message_id'] == message_id:
            target_message = message
            
    if not channel_member_check(target_message['channel_id'], token):
        raise AccessError("Authorised user is not a member of channel with channel_id")
    
    # error
    authorised_user_id = token_to_uid(token)
    channel_id = target_message['channel_id']
    is_owner = False
    
    for channel in channels:
        if channel['channel_id'] == channel_id:
            target_channel = channel
    
    for owner in target_channel['owners']:
        if owner['u_id'] == authorised_user_id:
            is_owner = True

    if is_owner = False:
        raise InputError("The authorised user is not an owner")
    
    if target_message['is_pin'] = False:
        raise InputError("Message with ID message_id is already unpinned")
    
    target_message['is_pin'] = False
    
    return {}
 

