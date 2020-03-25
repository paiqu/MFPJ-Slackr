'''Route implementation for message_sendlater'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, channel_member_check, channel_id_check
from error import InputError
from class_file import User
from data import DATA, getData ,MESSAGE_COUNT
import time, datetime

SENDMESSAGELATER = Blueprint('message_sendlater', __name__)

@SENDMESSAGELATER.route('/message/sendlater', methods=['Post'])
def request_get():
    '''request get for route message sendlater'''
    request = request.get_json()
    token = request['token']
    channel_id = request['channel_id']
    message_content = request['message']
    time_send = request['time_send']
    message_send(token, channel_id, message_content, time_send)
    return dumps({})

def message_send(token, channel_id, message_content, time_send):
    ''' Send a message from authorised_user to the channel specified by channel_id'''
    if(len(message_content) > 1000):
        raise InputError('invalid message content')

    if not channel_member_check(channel_id, token):
        raise AccessError("Authorised user is not a member of channel with channel_id")
    
    if not channel_id_check(channel_id):
        raise InputError('Channel ID is not a valid channel')
    
    currenttime = time.time()
    
    if time_send < currenttime:
        raise InputError('Time sent is a time in the past')
        
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    messages = DATA['messages']
    
    global CHANNELS_COUNT
    CHANNELS_COUNT += 1
    message_id = CHANNELS_COUNT
    
    message_send = vars(Message(message_content, message_id, channel_id, token_to_uid(token)))
    
    returnvalue = {}
    returnvalue['message_id'] = message_id
    
    return returnvalue



    
    


