'''Route implementation for channel/details'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check
from error import InputError, AccessError

from data import getData



DETAILS = Blueprint('details', __name__)

@DETAILS.route('/channel/details', methods=['GET'])

def details():
    '''
    This function collects the information/parameters and calls the channel_details function
    '''

    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))

    # must return { name, owner_members, all_members }
    return dumps(channel_details(token, channel_id))

def channel_details(token, channel_id):
    '''
    Prints the channel details if the channel is valid, user is valid
    '''
    DATA = getData()
    #users = DATA['users']
    channels = DATA['channels']


    # Discovers the user from the token parameter
    #for user in users:
        #if user['u_id'] == token_to_uid(token):
            #request_user = user


    # Find the channel which the channel ID belongs to
    for channel in channels:
        if channel['channel_id'] == channel_id:
            target_channel = channel


    # Checks the Target Channel ID is not invalid
    if not channel_id_check(target_channel['channel_id']):
        raise InputError("This is not a valid channel or channel ID")

    # Checks the Invitee/Token User is member of the channel
    if not channel_member_check(channel_id, token):
        raise AccessError("The user requesting channel details is not a member of this channel")

    owner_members_list = []
    all_members_list = []

    for owner in target_channel['owners']:
        owner_dict = {
            'u_id' : owner['u_id'],
            'name_first' : owner['name_first'],
            'name_last' : owner['name_last']
        }
        owner_members_list.append(owner_dict)

    for member in target_channel['members']:
        member_dict = {
            'u_id' : member['u_id'],
            'name_first' : member['name_first'],
            'name_last' : member['name_last']
        }
        all_members_list.append(member_dict)
    return {
                'name': target_channel['channel_name'],

                'owner_members' : owner_members_list,

                'all_members' : all_members_list

        }
