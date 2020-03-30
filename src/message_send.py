'''Route implementation for message_send'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid
from error import InputError, AccessError
from data import DATA, getData
import time, datetime
from class_file import User, Channel, Message

SENDMESSAGE = Blueprint('message_send', __name__)

@SENDMESSAGE.route('/message/send', methods=['POST'])
def request_get():
    '''request get for route message send'''
    info = request.get_json()
    token = info['token']
    channel_id = info['channel_id']
    message = info['message']

    return dumps(message_send(token, channel_id, message))

def message_send(token, channel_id, message):
    '''Send a message from authorised_user to the channel specified by channel_id'''

    DATA = getData()
    users = DATA['users']
    messages = DATA['messages']   
    channels = DATA['channels']
    
    '''
    self check functions 
    users.append(vars(User(u_id=123, email='123@55.com', name_first='pai', name_last='qu', handle='')))   
    channels.append(vars(Channel(1,"Public")))
    channels[0]['members'].append(users[0])
    channels[0]['owners'].append(users[0])
    '''
    
    if(len(message) > 1000):
        raise InputError('invalid message content')
    
    is_member = False
    for user in users:
        if user['u_id'] == token_to_uid(token):
            target_member = user
            
    for channel in channels:
        if channel['channel_id'] == channel_id:
            global find_channel
            find_channel = channel
            
    for member in find_channel['members']:
        if member['u_id'] ==  target_member['u_id']:
            is_member = True
    
    if is_member == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")
    
    
    # get message_id  
    DATA['messages_count'] += 1
    message_id = DATA['messages_count']
    
    # get current time and send message
    now = datetime.datetime.utcnow()
    current_time = int(now.replace(tzinfo = datetime.timezone.utc).timestamp())
    target_message = vars(Message(message, message_id, channel_id, token_to_uid(token), int(current_time)))
    DATA['messages'].append(target_message)
    
    returnvalue = {}
    returnvalue['message_id'] = message_id
    
    return returnvalue

