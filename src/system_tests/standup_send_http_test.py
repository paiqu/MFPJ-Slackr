'''
This file is HTTP test for standup/send (POST)

Parameter: (token, channel_id, message)
Return: {}

Always reset workspace when testing!!!!!!!!

Steps to test standup/start:
    1. Register a user
    2. The user login to the server
    3. the user create a channel
    4. Time to Test:
        1. test for collecting messages successfully
        2. test fot Error:
            Raise InputError when channel_id is not valid
            Raise InputError when standup has not running in this channel
            Raise InputError when message is more than 1000 cahracters
            Raise AccessError when user is not the member of channel
'''
import sys
sys.path.append('..')
from json import load, dumps
import urllib.request
import urllib.parse
import pytest


PORT_NUMBER = '5204'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER
#BASE_URL now is 'http://127.0.0.1:5321'

@pytest.fixture
def register_and_login_user_1():
    '''
    register and login user one
    '''
    # RESET
    req = urllib.request.Request(
        f'{BASE_URL}/workspace/reset',
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    #Register user_1
    register_info = dumps({
        'email': 'z1234567@unsw.edu.au',
        'password': 'thisisaPassword',
        'name_first': 'Xinlei',
        'name_last': 'Matthew'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    # REGISTER user_2
    register_info_2 = dumps({
        'email': 'z7654321@unsw.edu.au',
        'password': 'thisisaPassword',
        'name_first': 'Pete',
        'name_last': 'Peteer'
    }).encode('utf-8')


    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info_2,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    #Login 1st user
    login_info = dumps({
        'email': 'z1234567@unsw.edu.au',
        'password': 'thisisaPassword'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    # Login user_2
    login_info = dumps({
        'email': 'z7654321@unsw.edu.au',
        'password': 'thisisaPassword'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

def create_public_channel(register_and_login_user_1):
    '''
    create a public channel
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1

    # Create a public channel
    channel_info = dumps({
        'token': user_1_token,
        'name': 'a channel',
        'is_public': True
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channels/create',
        data=channel_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    payload = load(urllib.request.urlopen(req))

def test_standup_send(register_and_login_user_1):
    '''
    This function is to send_standup whether can store message
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    create_public_channel(register_and_login_user_1)

    # Set one channel
    channel_info = dumps({
        'token': user_1_token,
        'channel_id': 1,
        'length': 500
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/standup/start',
        data=channel_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    standup_info = dumps({
        'token': user_1_token,
        'channel_id': 1,
        'message': 'You are so smart!'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/standup/send',
        data=standup_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    payload = load(urllib.request.urlopen(req))
    assert payload == {}

def test_invalid_channel_id(register_and_login_user_1):
    '''
    This function is test whether the channel_id is valid
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    create_public_channel(register_and_login_user_1)

    # Set standup state
    channel_info = dumps({
        'token': user_1_token,
        'channel_id': 2,
        'length': 500
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/standup/start',
        data=channel_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_standup_send_message_long(register_and_login_user_1):
    '''
    This function is to send long message
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    create_public_channel(register_and_login_user_1)

    # Set one channel
    channel_info = dumps({
        'token': user_1_token,
        'channel_id': 1,
        'length': 500
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/standup/start',
        data=channel_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    standup_info = dumps({
        'token': user_1_token,
        'channel_id': 1,
        'message': 'You are so smart!' * 1000
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/standup/send',
        data=standup_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_standup_send_notrunning_channel(register_and_login_user_1):
    '''
    This function is to check the standup whether is running in channel
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    create_public_channel(register_and_login_user_1)
    create_public_channel(register_and_login_user_1)

    # Set one channel
    channel_info = dumps({
        'token': user_1_token,
        'channel_id': 1,
        'length': 500
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/standup/start',
        data=channel_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    standup_info = dumps({
        'token': user_1_token,
        'channel_id': 2,
        'message': 'You are so smart!'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/standup/send',
        data=standup_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_for_access_error(register_and_login_user_1):
    '''
    This function is check the AccessError
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''

    create_public_channel(register_and_login_user_1)

    # Set one channel
    channel_info = dumps({
        'token': user_1_token,
        'channel_id': 1,
        'length': 500
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/standup/start',
        data=channel_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    standup_info = dumps({
        'token': user_2_token,
        'channel_id': 1,
        'message' : 'You are so smart!'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/standup/send',
        data=standup_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
