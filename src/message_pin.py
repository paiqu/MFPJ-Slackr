'''Route implementation for message_pin'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, channel_member_check, message_id_check
from error import InputError, AccessError
from data import DATA, getData
from class_file import User, Channel, Message

PIN = Blueprint('message_pin', __name__)

@PIN.route('/message/pin', methods=['POST'])
def request_get():
    '''request get for route message pin'''
    info = request.get_json()
    token = info['token']
    message_id = int(info['message_id'])
    
    return dumps(message_pin(token, message_id))

def message_pin(token, message_id):
    ''' Given a message within a channel, mark it as "pinned" to be given special display treatment by the frontend'''

    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    messages = DATA['messages']

    users.append(vars(User(u_id=123, email='123@55.com', name_first='pai', name_last='qu', handle='')))   
    channels.append(vars(Channel(1,"Public")))
    channels[0]['members'].append(users[0])
    channels[0]['owners'].append(users[0])
    messages.append(vars(Message("hello",1,1,123,574820)))

    if not message_id_check(message_id):
        raise InputError("message_id is not a valid message")

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

    if is_owner == False:
        raise InputError("The authorised user is not an owner")
    
    if target_message['is_pin'] == True:
        raise InputError("Message with ID message_id is already pinned")
    
    target_message['is_pin'] = True
    
    return target_message
 

