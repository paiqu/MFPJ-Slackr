'''Route implementation for message_send'''
import datetime
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, channel_member_check
from error import InputError, AccessError
from data import getData
from class_file import Message

SENDMESSAGE = Blueprint('message_send', __name__)

@SENDMESSAGE.route('/message/send', methods=['POST'])
def request_get():
    '''request get for route message send'''
    info = request.get_json()
    token = info['token']
    channel_id = int(info['channel_id'])
    message = info['message']

    return dumps(message_send(token, channel_id, message))

def message_send(token, channel_id, message):
    '''Send a message from authorised_user to the channel specified by channel_id'''

    DATA = getData()

    if len(message) > 1000:
        raise InputError('invalid message content')

    if not channel_member_check(channel_id, token):
        raise AccessError("Authorised user is not a member of channel with channel_id")

    # get message_id
    DATA['messages_count'] += 1
    message_id = DATA['messages_count']

    # get current time and send message
    now = datetime.datetime.utcnow()
    current_time = int(now.replace(tzinfo=datetime.timezone.utc).timestamp())
    DATA['messages'].append(vars(Message(message, message_id, channel_id, token_to_uid(token), int(current_time))))

    returnvalue = {}
    returnvalue['message_id'] = message_id

    return returnvalue
