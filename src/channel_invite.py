'''Route implementation for channel/invite'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid, user_id_check
from error import InputError, AccessError
from token_functions import generate_token

from data import DATA, getData

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
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']

    ###Need to add a function for in case the user of token is not verified to invite other users 


    # Finds the user which the token belongs to  
    # This user must already be a member of the channel 
    for user in users:
        if user['u_id'] == token_to_uid(token):
            member_user = user

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
    
    owners = target_channel['owners']

    # Checks the Target Channel ID is not invalid
    if channel_id_check(target_channel) == False:
        raise InputError("This is not a valid channel or channel ID")

    # Checks the User ID is not invalid
    if user_id_check(u_id) == False:
        raise InputError("This is not a valid user or user ID")

    # Checks the Invitee/Token User is member of the channel 
    if channel_member_check(channel_id,token) == False:
        raise AccessError("The invitee is not a member of this channel")

    # Checks the Invited User is not already a member of the channel
    if channel_member_check(channel_id, target_user['token']) == True:
        raise AccessError("The user is already a memeber in this channel")
                    
    members = target_channel['members']
    members.append(target_user)
          
     
        
    return {}

