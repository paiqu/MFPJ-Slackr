''' Route implementation for channels/route'''
from json import dumps
from flask import Blueprint, request
from data import DATA, getData

CHANNELS_LISTALL = Blueprint('channels_listall', __name__)

@CHANNELS_LISTALL.route('/channels/listall', methods=['GET'])
def listall():
    ''' function for route channels/list '''
    token = request.args.get('token')
    return dumps(channels_listall(token))

def channels_listall(token):
    '''
    Given a token, list all channels
    '''
    global DATA
    DATA = getData()
    new_list = []
    for channel in DATA['channels']:
        new_dict = {}
        new_dict['channel_id'] = channel['channel_id']
        new_dict['name'] = channel['channel_name']
        new_list.append(new_dict)

    return_dict = {}
    return_dict['channels'] = new_list
    return return_dict
