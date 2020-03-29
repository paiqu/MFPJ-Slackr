'''Route implementation for channel/leave'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError

from data import DATA, getData

LEAVE = Blueprint('leave', __name__)

@LEAVE.route('/channel/leave', methods=['POST'])
def leave():
    '''function for route channle/leave'''
    info = request.get_json()
    token = info['token']
    channel_id = info['channel_id']
    #channel_id = request.form.get('channnel_id')

    channel_leave(token, channel_id)
    return dumps({})


def channel_leave(token, channel_id):
    '''
    Given a channel ID, the user removed as a member of this channel

    Input Error:
        invlid channel_id
    Access Error:
        authorised user is not a member of channel with channel_Id

    ASSUME: the token id is valid
    '''
   
    if not channel_id_check(channel_id):
        raise InputError("Invalid channel_id")

    if not channel_member_check(channel_id, token):
        raise AccessError("Authorised user is not a member of channel with channel_id")

    DATA = getData()


    for channel in DATA['channels']:
        if channel['channel_id'] == channel_id:
            for user in DATA['users']:
                if user['u_id'] == token_to_uid(token):
                    channel['members'].remove(user)

    return {}
