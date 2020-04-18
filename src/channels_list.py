'''Route implementation for channel/list'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_member_check
from data import DATA, getData

CHANNELS_LIST = Blueprint('channels_list', __name__)

@CHANNELS_LIST.route('/channels/list', methods=['GET'])
def route_channels_list():
    '''function for route channels/list'''
    token = request.args.get('token')
    return dumps(channels_list(token))

def channels_list(token):
    '''
    Given a token, list all channels that user is a part of
    '''

    global DATA
    DATA = getData()
    new_list = []
    for channel in DATA['channels']:
        if channel_member_check(channel['channel_id'], token):
            new_dict = {}
            new_dict['channel_id'] = channel['channel_id']
            new_dict['name'] = channel['channel_name']
            new_list.append(new_dict)

    return_dict = {}
    return_dict['channels'] = new_list
    return return_dict
