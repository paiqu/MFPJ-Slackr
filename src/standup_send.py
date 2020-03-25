from json import dumps
from flask import Blueprint, request
from check_error import token_check, channel_id_check, active_check
from error import InputError, AccessError
from check_functions import token_to_uid

from class_file import User
from data import *
import datetime

SEND = Blueprint('send', __name__)

@SEND.route('/send', methods=['POST'])
def start():
    store = request.get_json()
    token = store['token']
    channel_id = int(store['channel_id'])
    message = store['message']

    return dumps(standup_start(token, channel_id, message))

def standup_start(token, channel_id, message):
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
    if active_check(channel_id, token, length) == False:
        raise InputError(" An active standup is not currently running in this channel")
    if channel_member_check(channel_id, token) == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")


    global DATA
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    messages = DATA['messages']
    start_times = DATA['times']
    
    curr = datetime.datetime.now()
    message_send = vars(Message(message, message_id, channel_id, token_to_uid(token), int(curr)))
    
    returnvalue = {}
    returnvalue['message'] = message.append(message_send)
    
    return {}
