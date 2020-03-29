from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError
from class_file import User, Channel
from data import DATA, getData, CHANNELS_COUNT
from token_functions import generate_token

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
    if(len(name) > 20):
        raise InputError('invalid channel name')
    
    is_private = False

    if is_public == "True":
        is_private = False
    elif is_public == "False":
        is_private = True

    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    '''
    # DELETE LATER
    user_1 = User(u_id=token_to_uid(token), email='123@55.com', name_first='pai', name_last='qu', handle='')
    user_1 = vars(user_1)
    ##############
    '''


    for user in users:
        if user['u_id'] == token_to_uid(token):
            target_user = user
    
    global CHANNELS_COUNT
    CHANNELS_COUNT += 1
    channel_id = CHANNELS_COUNT

    target_channel = vars(Channel(channel_id=CHANNELS_COUNT, channel_name=name))
    target_channel['members'].append(target_user)
    target_channel['owners'].append(target_user)

    if is_private:
        target_channel['is_public'] = False

    channels.append(target_channel)

    return_dict = {}
    return_dict['channel_id'] = channel_id
    

    return channels
    