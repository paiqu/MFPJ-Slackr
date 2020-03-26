
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError

from data import DATA, getData

CHANNEL_MESSAGES = Blueprint('channel_messages', __name__)

@CHANNEL_MESSAGES.route('/channel/messages', method=['GET'])
def route_channel_messages():
    # function for route channel/messages
    token = request.args.get('token')
    channel_id = request.args.get('channnel_id')
    start = request.args.get('start')
    
    return dumps(channel_messages(token, channel_id, start))

def channel_messages(token, channel_id, start):
    # assume token is valid
    
    if not channel_id_check(channel_id):
        raise InputError("Invalid channel_id")
    
    if start > len(DATA['messages'])
        raise InputError("Invalid start")
        
    if not channel_member_check(channel_id, token):
        raise AccessError("Authorised user is not a member of channel with channel_id")
    
    DATA = getData()
    messages_list = DATA['messages']
    
    out_dict = {}
    mess_output = []
    
    if start + 50 > len(messages_list):
        for i in range(len(messages_list)):
            mess_output.append(messages_list[i]) 
        out_dict['end'] = -1
        
    else: 
        for i in range(50):
            mess_output.append(messages_list[i])
        out_dict['end'] = start + 50   
    
    out_dict['messages'] = mess_output
    out_dict['start'] = start
    
    return out_dict
        
    
