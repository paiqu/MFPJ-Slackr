'''
Server implementation for channels/create
'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid
from error import InputError
from class_file import Channel
from data import getData


CREATE = Blueprint('create', __name__)


@CREATE.route('/channels/create', methods=['POST'])
def create():
    '''function for route channle/leave'''
    info = request.get_json()
    token = info['token']
    name = info['name']
    is_public = info['is_public']


    return dumps(channels_create(token, name, is_public))

def channels_create(token, name, is_public):
    ''' function to create a channel'''
    if len(name) > 20:
        raise InputError('invalid channel name')

    is_private = False

    if is_public:
        is_private = False
    elif not is_public:
        is_private = True

    DATA = getData()
    users = DATA['users']


    for user in users:
        if user['u_id'] == token_to_uid(token):
            target_user = user


    DATA['channels_count'] += 1

    channel_id = DATA['channels_count']

    target_channel = vars(Channel(channel_id=channel_id, channel_name=name))
    target_channel['members'].append(target_user)
    target_channel['owners'].append(target_user)

    if is_private:
        target_channel['is_public'] = False

    DATA['channels'].append(target_channel)

    return_dict = {}
    return_dict['channel_id'] = channel_id

    return return_dict
    