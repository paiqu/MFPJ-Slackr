'''Route implementation for channel/details'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError
from token_functions import generate_token

from data import DATA, getData



DETAILS = Blueprint('details', __name__)

@DETAILS.route('/channel/details', methods=['GET'])

def details():
    '''
    This function collects the information/parameters and calls the channel_details function
    '''
    info = request.get_json()
    token = info['token']
    channel_id = int(info['channel_id'])

    # must return { name, owner_members, all_members }
    return dumps(channel_details(token, channel_id))

def channel_details(token, channel_id):
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']


    # Discovers the user from the token parameter 
    for user in users:
        if user['u_id'] == token_to_uid(token):
            request_user = user
        
        channel = {'channel':{}}
    
    # Find the channel which the channel ID belongs to 
    for channel in channels:
        if channel['channel_id'] == channel_id:
            target_channel = channel

    
    # Checks the Target Channel ID is not invalid 
    if channel_id_check(target_channel) == False:
        raise InputError("This is not a valid channel or channel ID")

    # Checks the Invitee/Token User is member of the channel 
    if channel_member_check(channel_id,token == False):
        raise AccessError("The user requesting channel details is not a member of this channel")
    
    return dumps({
                'name': channel['name'],

                # Can I call this considering member list is a list???
                'owner_members' : channel['owner_members'],
                'all_members' : channel['all_members']

            })
             
         
            
            
    
        
    
            
   
