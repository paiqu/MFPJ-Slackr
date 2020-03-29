'''Route implementation for message_remove'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, channel_member_check, message_id_check
from error import InputError, AccessError
from data import DATA, getData
from class_file import User, Channel, Message

REMOVE = Blueprint('message_remove', __name__)

@REMOVE.route('/message/remove', methods=['DELETE'])
def request_get():
    '''request get for route message romove'''
    info = request.get_json()
    token = info['token']
    message_id = int(info['message_id'])
    
    return dumps(message_remove(token, message_id))

def message_remove(token, message_id):
    '''Given a message_id for a message, this message is removed from the channel'''

    authorised_user = token_to_uid(token)
    
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    messages = DATA['messages']
    
    '''
    self check function
    users.append(vars(User(u_id=123, email='123@55.com', name_first='pai', name_last='qu', handle='')))   
    channels.append(vars(Channel(1,"Public")))
    channels[0]['members'].append(users[0])
    channels[0]['owners'].append(users[0])
    messages.append(vars(Message("hello",1,1,123,574820)))
    '''
    
    if not message_id_check(message_id):
        raise InputError("message_id is not a valid message")
    
    # find the target_message
    for message in messages:
        if message['message_id'] == message_id:
            target_message = message
    
    # check whether the user is owner, sender or slack owner            
    channel_id = target_message['channel_id']
    is_owner = False
    is_sender = False
    is_slack_owner = False
    
    if target_message['sender_id'] == authorised_user:
        is_sender = True
    
    # find the target channel         
    for channel in channels:
        if channel['channel_id'] == channel_id:
            target_channel = channel
    
    for owner in target_channel['owners']:
        if owner['u_id'] == authorised_user:
            is_owner = True
    
    for user in users:
        if user['u_id'] == authorised_user:
            if user['is_slack_owner'] == True:
                is_slack_owner = True
    
    if is_owner == False and is_sender == False and is_slack_owner == False:
        raise AccessError("You are not this channel owner,this message sender and slack owner ")
    
    # remove this message
    messages.remove(target_message)
    
    return {}

