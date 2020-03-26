'''
This file is to store function:
    token_check(token) --  Check for valid token

    channel_id_check(channel_id) -- Check for valid channel_id

    channel_member_check(token, channel_id) 
        -- Check if a memeber with token is in channel with channel_id

'''
from data import *
import jwt

def token_check(token):
    ''' Return True if the token is valid '''
    return False

def channel_id_check(channel_id):
    ''' Return True is the channel_id is valid ''' 
    DATA = getData()

    channels = DATA['channels']
    for channel in channels:
        if channel['channel_id'] == channel_id:
            return True
    
    return False

def channel_member_check(channel_id, token):
    ''' Return True is member with token is in channel with channel_id'''
    DATA = getData()

    channels = DATA['channels']
    users = DATA['users']

    for channel in channels:
        if channel['channel_id'] == channel_id:
            target_channel = channel

    for user in users:
        if user['u_id'] == token_to_uid(token):
            target_member = user

    for member in target_channel['members']:
        if member['u_id'] == target_member['u_id']:
            return True

    return False

def token_to_uid(token):
    ''' Convert a token to u_id '''
    global SECRET
    decoded = jwt.decode(token[2:-1], SECRET, algorithms=['HS256'])
    return int(decoded['u_id'])

def message_id_check(message_id):
    ''' Return True is the message_id is valid ''' 
    DATA = getData()

    messages = DATA['messages']
    for message in messages:
        if message['message_id'] == message_id:
            return True
    
    return False
