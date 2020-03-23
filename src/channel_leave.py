'''Route implementation for channel/leave'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError

from class_file import Channel
from data import *

LEAVE = Blueprint('leave', __name__)

@LEAVE.route('/leave', methods=['POST'])
def leave():
    '''function for route channle/leave'''
    token = request.form.get('token')
    channel_id = request.form.get('channnel_id')

    return dumps(channel_leave(token, channel_id))


def channel_leave(token, channel_id):
    '''
    Given a channel ID, the user removed as a member of this channel

    Input Error:
        invlid channel_id
    Access Error:
        authorised user is not a member of channel with channel_Id
    
    ASSUME: the token id is valid
    '''

    if channel_id_check(channel_id) == False:
        raise InputError("Invalid channel_id")

    if channel_member_check(channel_id, token) == False:
        raise AccessError("Authorised user is not a member of channel with channel_id")

    global DATA
    DATA = getData()



    for channel in DATA['channels']:
        if channel.channel_id == channel_id:
            for user in DATA['users']:
                if user.u_id == token_to_uid(token):
                    channel.members.remove(user)
    
    return {}



       




    


