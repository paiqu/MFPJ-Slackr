'''Route implementation for message_sendlater'''
import datetime
import threading
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, channel_member_check, channel_id_check
from error import InputError, AccessError
from data import getData
from class_file import Message

SENDMESSAGELATER = Blueprint('message_sendlater', __name__)

@SENDMESSAGELATER.route('/message/sendlater', methods=['POST'])
def request_get():
    '''request get for route message sendlater'''
    info = request.get_json()
    token = info['token']
    channel_id = int(info['channel_id'])
    message = info['message']
    time_sent = int(info['time_sent'])

    return dumps(message_sendlater(token, channel_id, message, time_sent))

def message_sendlater(token, channel_id, message, time_sent):
    ''' Send a message from authorised_user to the channel specified by channel_id'''
    DATA = getData()

    if len(message) > 1000:
        raise InputError('invalid message content')

    if not channel_id_check(channel_id):
        raise InputError('Channel ID is not a valid channel')

    if not channel_member_check(channel_id, token):
        raise AccessError("Authorised user is not a member of channel with channel_id")

    now = datetime.datetime.utcnow()
    currenttime = int(now.replace(tzinfo=datetime.timezone.utc).timestamp())

    if time_sent < int(currenttime):
        raise InputError('Time sent is a time in the past')

    DATA['messages_count'] += 1
    message_id = DATA['messages_count']

    u_id = token_to_uid(token)

    def message_send(message, message_id, channel_id, u_id, time_sent):
        DATA['messages'].append(vars(Message(message, message_id, channel_id, u_id, time_sent)))

    # set a time to run this function
    time_diffrence = time_sent - currenttime
    timer = threading.Timer(time_diffrence, message_send, args=(message, message_id, channel_id, u_id, time_sent))
    timer.start()

    returnvalue = {}
    returnvalue['message_id'] = message_id
    return returnvalue
