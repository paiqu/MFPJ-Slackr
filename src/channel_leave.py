'''Route implementation for channel/leave'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check
from error import InputError, AccessError

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

    '''
    PSEUDOCODE:
    Assume we have written a channel class:
                    class Channel:
                        def __init__(self, channel_id):
                            self.channel_id = channel_id
                            self.members = []
                            self.owners []

    channel_1 = Channel(channel_id)

    member_list = channel_1.members
    member_list.remove(u_id) # u_id is the user id of the member with token

    return {}
    '''
    


