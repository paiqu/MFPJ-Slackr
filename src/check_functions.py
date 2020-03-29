'''
This file is to store function:
    token_check(token) --  Check for valid token

    channel_id_check(channel_id) -- Check for valid channel_id

    channel_member_check(token, channel_id) 
        -- Check if a memeber with token is in channel with channel_id

slackr_owner_permission = 1
slackr_member_permission = 2
owner_channel_permission = 3
member_channel_permission = 4
'''

from data import *
import jwt
import re
from token_functions import generate_token

def token_check(token):
    ''' Return True if the token is valid '''
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

def token_to_uid(token):
    ''' Convert a token to u_id '''
    global SECRET
    token_in_str = token[2:-1]
    token_in_byte = token_in_str.encode()
    decoded = jwt.decode(token_in_str, SECRET, algorithms=['HS256'])
    return int(decoded['u_id'])

def message_id_check(message_id):
    ''' Return True is the message_id is valid ''' 
    DATA = getData()

    messages = DATA['messages']
    for message in messages:
        if message['message_id'] == message_id:
            return True
    
    return False

def user_id_check(u_id):
    ''' Return True is the user_id is valid ''' 
    DATA = getData()

    users = DATA['users']
    for user in users:
        if user['u_id'] == u_id:
            return True
    
    return False

def user_exists_check(email):
    ''' Return True is the email is reigstered to an account ''' 
    DATA = getData()

    users = DATA['users']
    for user in users:
        if user['email'] == email:
            return True
    
    return False

if __name__ == '__main__':
    
    print (token_to_uid(b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg'))
    print(type(token_to_uid(b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg')))



