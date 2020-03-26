from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import AccessError
from class_file import Channel, Message
from data import DATA, getData

MESSAGE_EDIT = Blueprint('message_edit', __name__)

@MESSAGE_EDIT.route('/message/edit', methods=[PUT])
def route_message_edit():
    info = request.get_json()
    token = info['token']
    message_id = info['message_id']
    message = info['message']
    
    return dumps(message_edit(token, message_id, message))
    
def message_edit(token, message_id, message):
    DATA = getData()
    
    channels = DATA['channels']
    messages = DATA['messages']
    
    for i in messages:
        # find the target_message's information
        if i['message_id'] == message_id:
            target_message = i
          
    for j in channels:
        # find whether the user is a owner of a channel or not 
        is_owner = False
        if j['channel_id'] == target_message['channel_id']:
            for owner in j['owners']:
                if (token_to_uid(token) == owner['u_id']):
                    is_owner = True
    
    if target_message['sender_id'] != token_to_uid(token) or is_owner == False:
        raise AccessError("Unauthorised user try to edit")
     
     target_message['message_content'] = message
     return {}
     
