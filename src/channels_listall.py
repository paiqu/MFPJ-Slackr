# Route implementation for channels/route
from json import dumps
from flask import Blueprint, request
from class_file import Channel, User
from data import DATA, getData

CHANNELS_LISTALL = Blueprint('channels_listall', __name__)

@CHANNELS_LISTALL.route('/channels/listall', methods=['GET'])
def listall():
    # function for route channels/list
    token = request.args.get('token')
    return dumps(channels_listall(token))
    
def channels_listall(token):
    '''
    Given a token, list all channels 
    
    '''
    
    global DATA
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    '''
    users.append(vars(User(u_id=1, email='123@55.com', name_first='mike', name_last='cop', handle='')))
    channels.append(vars(Channel(channel_id = 1, channel_name = 'name')))
    channels[0]['members'].append(users[0])
    channels[0]['owners'].append(users[0])
    
    channels.append(vars(Channel(channel_id = 2, channel_name = 'NAME')))
    '''        
    return_dict = {}        
    return_dict['channels'] = channels
    return return_dict
