from json import dumps
from flask import Blueprint, request
from check_error import token_check, channel_id_check, active_check
from error import InputError, AccessError
from check_functions import token_to_uid

from class_file import User
from data import *
import datetime

ACTIVE = Blueprint('active', __name__)

@ACTIVE.route('/active', methods=['GET'])
def active():
    store = request.get_json()
    token = store['token']
    channel_id = int(store['channel_id'])

    return dumps(standup_active(token, channel_id))

def standup_active(token, channel_id):
    '''
    Input Error:
        channel_id is not valid

    ASSUME: the token id is valid
    '''  
    if channel_id_check(channel_id) == False:
        raise InputError("Invalid channel_id")
    
    global DATA
    DATA = getData()
    channels = DATA['channels']
    start_times = DATA['times']
    end_times = DATA['times']

    for user in DATA['users']:
        if user.u_id == token_to_uid(token):
            time_finish = end_times
    is_active = False

    curr = datetime.datetime.now()
    start = datetime.datetime.strptime(str(datetime.datetime.now().date()) + start_times, '%Y-%m-%d%H:%M')
    end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + end_times, '%Y-%m-%d%H:%M')

    if curr > start and curr < end:
        is_active = True
    else:
        is_active = False

    if is_active == True:
        return {is_active, time_finish}

    return {}