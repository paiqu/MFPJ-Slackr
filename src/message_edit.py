'''Route implement for message_edit'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid
from error import AccessError
# from class_file import Channel, Message, User
from data import DATA

MESSAGE_EDIT = Blueprint('message_edit', __name__)

@MESSAGE_EDIT.route('/message/edit', methods=['PUT'])
def route_message_edit():
    '''function for route message_edit'''
    info = request.get_json()
    token = info['token']
    message_id = int(info['message_id'])
    message = info['message']
    return dumps(message_edit(token, message_id, message))

def message_edit(token, message_id, message):
    '''
    Given a message, update it's text with new text.
    If the new message is an empty string, the message is deleted.
    '''
    global DATA
    channels = DATA['channels']
    messages = DATA['messages']

    for i in messages:
        # find the target_message's information
        if i['message_id'] == message_id:
            target_message = i

    is_owner = False
    for j in channels:
        # find whether the user is a owner of a channel or not
        if j['channel_id'] == target_message['channel_id']:
            for owner in j['owners']:
                if token_to_uid(token) == owner['u_id']:
                    is_owner = True

    if target_message['sender_id'] != token_to_uid(token) and is_owner == False:
        raise AccessError("Unauthorised user try to edit")

    if message == '':
        # empty string, delete message
        messages.remove(target_message)
    else:
        # update
        target_message['message_content'] = message
    return {}
