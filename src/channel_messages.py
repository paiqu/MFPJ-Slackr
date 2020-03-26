
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError
from class_file import User, Message, Channel
from data import DATA, getData

CHANNEL_MESSAGES = Blueprint('channel_messages', __name__)

@CHANNEL_MESSAGES.route('/channel/messages', methods=['GET'])
def route_channel_messages():
    # function for route channel/messages
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    
    return dumps(channel_messages(token, channel_id, start))

def channel_messages(token, channel_id, start):
    # assume token is valid
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    messages_list = DATA['messages']
    
    # delete later
    users.append(vars(User(u_id=1, email='123@55.com', name_first='mike', name_last='cop', handle='')))
    channels.append(vars(Channel(channel_id = 1, channel_name = 'name')))
    channels[0]['members'].append(users[0])
    channels[0]['owners'].append(users[0])
    messages_list.append(vars(Message(message_content = 'first', message_id = 1, channel_id = 1, sender_id = 1, time = 1231)))
    
    
    if not channel_id_check(channel_id):
        raise InputError("Invalid channel_id")

    if start > len(DATA['messages']):
        raise InputError("Invalid start")
        
    if not channel_member_check(channel_id, token):
        raise AccessError("Authorised user is not a member of channel with channel_id")

    out_dict = {}
    mess_output = []
    
    if start + 50 > len(messages_list):
        for i in range(len(messages_list)):
            mess_output.append(messages_list[i]) 
        out_dict['messages'] = mess_output
        out_dict['start'] = start
        out_dict['end'] = -1
        
    else: 
        for i in range(50):
            mess_output.append(messages_list[i])
        out_dict['messages'] = mess_output
        out_dict['start'] = start
        out_dict['end'] = start + 50   
    
    
    return out_dict
    
