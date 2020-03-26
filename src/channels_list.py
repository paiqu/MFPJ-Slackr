# Route implementation for channels/route
from json import dumps
from flask import Blueprint, request
from check_functions import channel_member_check
from class_file import Channel, User
from data import DATA, getData

CHANNELS_LIST = Blueprint('channels_list', __name__)

@CHANNELS_LIST.route('/channels/list', methods=['GET'])
def route_channels_list():
    # function for route channels/list
    token = request.args.get('token')
    return dumps(channels_list(token))
    
def channels_list(token):
    '''
    Given a token, list all channels that user is a part of 
    
    '''
    
    global DATA
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    
    users.append(vars(User(u_id=1, email='123@55.com', name_first='mike', name_last='cop', handle='')))
    channels.append(vars(Channel(channel_id = 1, channel_name = 'name')))
    channels[0]['members'].append(users[0])
    channels[0]['owners'].append(users[0])
    
    new_list = []
    for channel in DATA['channels']:
        if channel_member_check(channel['channel_id'], token):
            new_list.append(channel)
    
    return_dict = {}        
    return_dict['channels'] = new_list
    return return_dict
