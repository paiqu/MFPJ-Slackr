import time
import datetime
from json import dumps
from datetime import timezone
from flask import Blueprint, request
from check_functions import token_check, channel_id_check, token_to_uid
from error import InputError, AccessError
from class_file import Standup
from data import *

START = Blueprint('start', __name__)

@START.route('/standup/start', methods=['POST'])
def start():
    '''function for route of standup start'''
    store = request.get_json()
    token = store['token']
    channel_id = int(store['channel_id'])
    length = int(store['length'])
    
    return dumps(standup_start(token, channel_id, length))

def standup_start(token, channel_id, length):
    '''
    Input Error:
        channel_id is not valid
        an active standup is currently running in this channel

    ASSUME: the token id is valid
    ''' 
    DATA = getData()
    standups = DATA['standups']
    channels = DATA['channels']
    if channel_id_check(channel_id) == False:
        raise InputError("Invalid channel_id")

    now = datetime.datetime.utcnow()
    time_start = int(now.replace(tzinfo = timezone.utc).timestamp())
    time_end = int(time_start + int(length))

    for channel in channels:
        if channel['channel_id'] == channel_id:
            if channel['is_standup_active'] == True:
                raise InputError("Standup is running in this channel")

    standups.append(vars(Standup(channel_id, time_end)))

    for channel in channels:
        if channel['channel_id'] == channel_id:
            channel['is_standup_active'] = True

    return time_end