from json import dumps
from flask import Blueprint, request
from check_error import token_check, channel_id_check, active_check
from error import InputError, AccessError
from check_functions import token_to_uid

from class_file import User
from data import *

START = Blueprint('start', __name__)

@START.route('/start', methods=['POST'])
def start():
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
    if channel_id_check(channel_id) == False:
        raise InputError("Invalid channel_id")
    if active_check(channel_id, token, length) == True:
        raise InputError("Active standup is running")
    global DATA
    DATA = getData()
    start_times = DATA['times']
    
    for user in DATA['users']:
        if user.u_id == token_to_uid(token):
            time_finish = start_times + length
    
    return {time_finish}