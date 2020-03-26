'''Route implementation for channel/details'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError
from token_functions import generateToken

from data import DATA, getData



DETAILS = Blueprint('invite', __name__)

@DETAILS.route('/channel/details', methods=['POST'])

def details():

    info = request.get_json()
    token = info['token']
    channel_id = int(info['channel_id'])
    return dumps(channel_details(token, channel_id))

def channel_details(token, channel_id):
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']


    for user in users:
        if user['u_id'] == token_to_uid(token):
            verified_user = user
        else: 
            raise AccessError("This user is not a member of this channel, thus can't access channel details")

        channel = {'channel':{}}
    
    for channel in DATA['channels']:
        if channel.channel_id == channel_id:
            channel['channels']['channel_id'] = channel.channel_id 
            channel['channels']['channel_name'] = channel.channel_name
            channel['channels']['members'] = channel.members

            ## As the channel owners is a list - am I calling this correctly 
            channel['channels']['owners'] = channel.owners

            channel['channels']['handle_str'] = channel.is_public
            
    return channel
