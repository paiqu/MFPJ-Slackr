from json import dumps
from flask import Blueprint, request
from check_functions import token_check, channel_id_check, token_to_uid
from error import InputError, AccessError
from class_file import User
from data import *
import datetime

ACTIVE = Blueprint('active', __name__)

@ACTIVE.route('/standup/active', methods=['GET'])
def active():
    '''function for route of standup active'''
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    return dumps(standup_active(token, channel_id))

def standup_active(token, channel_id):
    '''
    Input Error:
        channel_id is not valid

    ASSUME: the token id is valid
    '''  

    DATA = getData()
    standups = DATA['standups']
    channels = DATA['channels']
    is_active = False

    if channel_id_check(channel_id) == False:
        raise InputError("Invalid channel_id")
    
    for channel in channels:
        if channel['channel_id'] == channel_id:
            if channel['is_standup_active'] == True:
                is_active = True
                for standup in standups:
                    if standup['channel_id'] == channel_id:
                        time_end = standup['time_end']
            else:
                is_active = False
                time_end = None
    returnlist = {}
    returnlist['is_active'] = is_active
    returnlist['time_finish'] = time_end

    return returnlist