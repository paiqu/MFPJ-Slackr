# Route implementation for channels/route
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError

from class_file import Channel
from data import *

LEAVE = Blueprint('channels_listall', __name__)

@LEAVE.route('/channels/listall', methods=['POST'])
    
def channels_listall(token):
    '''
    Given a token, list all channels 
    
    '''
    new_list = []
    
    global DATA
    DATA = getData()
    
    for user in DATA['users']: 
        if user.u_id == token_to_uid(token):
            return DATA['channels']
        
        
        '''if channel_member_check(channel.channel_id, token):
            new_dict = {}
            new_dict['channel_id'] = channel.channel_id
            new_dict['name'] = channel.name
            new_list.append(new_dict)
            
    return_dict['channels'] = new_list
    return return_dict
         '''   
    
    
def listall():
    # function for route channels/list
    token = request.form.get('token')
    channel_id = request.form.get('channnel_id')
    return dumps(channels_list(token, channel_id))
