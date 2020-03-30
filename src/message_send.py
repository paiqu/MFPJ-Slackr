'''Route implementation for message_send'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, channel_member_check
from error import InputError, AccessError
from data import DATA, getData, MESSAGE_COUNT
import time, datetime
from class_file import User, Channel, Message

SENDMESSAGE = Blueprint('message_send', __name__)

@SENDMESSAGE.route('/message/send', methods=['POST'])
def request_get():
    '''request get for route message send'''
    info = request.get_json()
    token = info['token']
    channel_id = info['channel_id']
    message_content = info['message_content']

    return dumps(message_send(token, channel_id, message_content))

def message_send(token, channel_id, message_content):
    '''Send a message from authorised_user to the channel specified by channel_id'''

    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    messages = DATA['messages']   
    
    '''
    self check functions 
    users.append(vars(User(u_id=123, email='123@55.com', name_first='pai', name_last='qu', handle='')))   
    channels.append(vars(Channel(1,"Public")))
    channels[0]['members'].append(users[0])
    channels[0]['owners'].append(users[0])
    '''
    
    if(len(message_content) > 1000):
        raise InputError('invalid message content')
    
    if not channel_member_check(channel_id, token):
        raise AccessError("Authorised user is not a member of channel with channel_id")
    
    # get message_id
    DATA['messages_count'] += 1
    message_id = DATA['messages_count']
    
    # get current time and send message
    now = datetime.datetime.utcnow()
    current_time = int(now.replace(tzinfo = datetime.timezone.utc).timestamp())
    messages.append(vars(Message(message_content, message_id, channel_id, token_to_uid(token), int(current_time))))
    
    returnvalue = {}
    returnvalue['message_id'] = message_id
    
    return returnvalue

