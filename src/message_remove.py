'''Route implementation for message_remove'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, channel_member_check, message_id_check
from error import InputError, AccessError
from data import DATA, getData

REMOVE = Blueprint('message_remove', __name__)

@REMOVE.route('/message/remove', methods=['Delete'])
def request_get():
    '''request get for route message romove'''
    request = request.get_json()
    token = request['token']
    message_id = int(request['message_id'])
    message_remove(token, message_id)
    return dumps({})

def message_remove(token, message_id):
    '''Given a message_id for a message, this message is removed from the channel'''

    if not message_id_check(message_id):
        raise InputError("message_id is not a valid message")
    
    authorised_user = token_to_uid(token)
    
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    messages = DATA['messages']

    for message in messages:
        if message['message_id'] == message_id:
            target_message = message
            
    channel_id = target_message['channel_id']
    is_owner = False
    is_sender = False
    is_slack_owner = False
    
    if target_message['sender_id'] = authorised_user:
        is_sender = True
              
    for channel in channels:
        if channel['channel_id'] == channel_id:
            target_channel = channel
    
    for owner in target_channel['owners']:
        if owner['u_id'] == authorised_user:
            is_owner = True
    
    for user in users:
        if user['u_id'] = authorised_user
            if user['is_slack_owner'] = True
                is_slack_owner = True
    
    if is_owner = False and is_sender = False and is_slack_owner = False
        raise AccessError("You are not this channel owner,this message sender and slack owner ")
    
    users.pop(target_message)
    
    return {}   
