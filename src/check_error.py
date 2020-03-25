import re
import jwt
import datetime
from data import *
from class_file import *

def token_check(token):
    return False

def check_email(email): 
    '''Return True is email is valid'''
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'  
    if(re.search(regex,email)):  
        return True  
    
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
def active_check(channel_id, token, length)
    '''Return Ture when current time is between start_time and end_time'''
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    messages = DATA['messages']
    start_times = DATA['times']

    curr = datetime.datetime.now()
    
    start = datetime.datetime.strptime(str(datetime.datetime.now().date()) + start_time, '%Y-%m-%d%H:%M')
    end = datetime.datetime.strptime(str(datetime.datetime.now().date()) + start_time + length, '%Y-%m-%d%H:%M')
    
    #judge whether current time is between start_time and end_time
    if curr > start and curr < end:
        return True
    
    return False