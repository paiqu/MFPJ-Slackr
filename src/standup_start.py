'''
Route for standup_start
'''
import datetime
from json import dumps
from datetime import timezone
import threading
from flask import Blueprint, request
from check_functions import channel_id_check, token_to_uid
from error import InputError
from class_file import Standup, Message
from data import getData

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
    DATA['messages_count'] += 1
    message_id = DATA['messages_count']

    if channel_id_check(channel_id) == False:
        raise InputError("Invalid channel_id")

    now = datetime.datetime.utcnow()
    time_start = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_end = int(time_start + int(length))

    for channel in channels:
        if channel['channel_id'] == channel_id:
            if channel['is_standup_active'] == True:
                raise InputError("Standup is running in this channel")

    standups.append(vars(Standup(channel_id, time_end)))

    for channel in channels:
        if channel['channel_id'] == channel_id:
            channel['is_standup_active'] = True

    u_id = token_to_uid(token)
    time_sent = time_end

    def message_send_all(message_id, channel_id, u_id, time_sent):
        '''
        This function is for message send
        '''
        message = ''
        DATA = getData()
        standups = DATA['standups']
        for standup in standups:
            if standup['channel_id'] == channel_id:
                for i in standup['messages']:
                    message = message + i + '\n'
        DATA['messages'].append(vars(Message(message, message_id, channel_id, u_id, time_sent)))
        for channel in channels:
            if channel['channel_id'] == channel_id:
                channel['is_standup_active'] = False

        for standup in standups:
            if standup['channel_id'] == channel_id:
                standups.remove(standup)

    timer = threading.Timer(length, message_send_all, args=(message_id, channel_id, u_id, time_sent))
    timer.start()
    return time_end
