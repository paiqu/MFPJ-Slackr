'''Route implementation for channel/invite'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, user_id_check
from error import InputError, AccessError

from data import getData

INVITE = Blueprint('invite', __name__)

@INVITE.route('/channel/invite', methods=['POST'])
def invite():
    '''
    This function collects the information/parameters and calls the channel_invite function
    '''
    info = request.get_json()
    token = info['token']

    channel_id = int(info['channel_id'])
    u_id = int(info['u_id'])
    # must return {}

    return dumps(channel_invite(token, channel_id, u_id))



def channel_invite(token, channel_id, u_id):
    '''
    Invites a user to a channel is the parameters are valid
    '''
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']

    ###Need to add a function for in case the user of token is not verified to invite other users


    # Finds the user which the token belongs to
    # This user must already be a member of the channel
    #for user in users:
        #if user['u_id'] == token_to_uid(token):
            #member_user = user

    # Finds the user which the user ID
    # This user is who we are intending to invite into the channel
    # The user must not already be a member of the channel
    for user in users:
        if user['u_id'] == u_id:
            target_user = user

    # Find the channel which the channel ID belongs to
    for channel in channels:
        if channel['channel_id'] == channel_id:
            target_channel = channel

    #owners = target_channel['owners']

    # Checks the Target Channel ID is not invalid
    if not channel_id_check(target_channel['channel_id']):
        raise InputError("This is not a valid channel or channel ID")

    # Checks the User ID is not invalid
    if not user_id_check(u_id):
        raise InputError("This is not a valid user or user ID")

    # Checks the Invitee/Token User is member of the channel
    if not channel_member_check(channel_id, token):
        raise AccessError("The invitee is not a member of this channel")

    # Checks the Invited User is not already a member of the channel
    if channel_member_check(channel_id, target_user['token']):
        raise AccessError("The user is already a memeber in this channel")

    members = target_channel['members']
    members.append(target_user)

    return {}
