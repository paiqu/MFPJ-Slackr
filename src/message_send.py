'''Route implementation for message_send'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, channel_member_check
from error import InputError, AccessError
from class_file import Message
from data import DATA, getData ,MESSAGE_COUNT

SENDMESSAGE = Blueprint('message_send', __name__)

@SENDMESSAGE.route('/message/send', methods=['Post'])
def request_get():
    '''request get for route message send'''
    request = request.get_json()
    token = request['token']
    channel_id = int(request['channel_id'])
    message_content = request['message']
    
    message_send(token, channel_id, message_content)
    return dumps({})

def message_send(token, channel_id, message_content):
    ''' Send a message from authorised_user to the channel specified by channel_id'''
    if(len(message_content) > 1000):
        raise InputError('invalid message content')

    if not channel_member_check(channel_id, token):
        raise AccessError("Authorised user is not a member of channel with channel_id")

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
 
