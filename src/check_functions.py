'''
This file is to store function:
    token_check(token) --  Check for valid token

    channel_id_check(channel_id) -- Check for valid channel_id

    channel_member_check(token, channel_id) 
        -- Check if a memeber with token is in channel with channel_id

'''
from data import *

def token_check(token):
    ''' Return True if the token is valid '''
    return False

def channel_id_check(channel_id):
    ''' Return True is the channel_id is valid ''' 
    global DATA
    DATA = getData()

    channels = DATA['channels']
    for channel in channels:
        if channel.channel_id == channel_id:
            return True
    
    return False

def channel_member_check(channel_id, token):
    ''' Return True is member with token is in channel with channel_id'''
    global DATA
    DATA = getData


    return False

def token_to_uid(token):
    ''' Convert a token to u_id '''
    global SECRET

    decoded = jwt.decode(token, SECRET, algorithms = ['HS256'])

    return decoded['u_id']
