'''
This file is HTTP test for standup/start (POST)

Parameter: (token, channel_id, length)
Return: {time_finish}

Always reset workspace when testing!!!!!!!!

Steps to test standup/start:
    1. Register a user
    2. The user login to the server
    3. the user create a channel
    4. Time to Test:
        1. test for returning time_finish successfully
        2. test fot Error:
            Raise InputError when channel_id is not valid
            Raise InputError when standup has been running in this channel
'''
import sys
sys.path.append('..')
from json import load, dumps
import urllib
import flask
import pytest
from data import *
from error import InputError, AccessError


PORT_NUMBER = '5321'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER
#BASE_URL now is 'http://127.0.0.1:5321'

@pytest.fixture
def register_and_login_user_1():
    # RESET
    req = urllib.request.Request(
        f'{BASE_URL}/workspace/reset',
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))
    
    #REGISTER user_1
    register_info = dumps({
        'email': 'z1234567@unsw.edu.au',
        'password': 'thisisaPassword',
        'name_first': 'Xinlei',
        'name_last': 'Matthew'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data = register_info,
        headers = {'Content-Type': 'application/json'},
        method = 'POST'
    )

    load(urllib.request.urlopen(req))

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

    #LOGIN user_1    
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

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    
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

def test_channel_invite_basic(register_and_login_user_1):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    create_public_channel(register_and_login_user_1)

    # Set a first and last name
    channel_info = dumps({
        'token': user_1_token,
        'channel_id': 1,
        'u_id': 2
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/invite',
        data = channel_info,
        headers = {'Content-Type': 'application/json'},
        method = 'POST'
    )
    payload = load(urllib.request.urlopen(req))
    assert payload == {}

'''
def test_invalid_channel_id(register_and_login_user_1):
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
        data = channel_info,
        headers = {'Content-Type': 'application/json'},
        method = 'POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_running_channel(register_and_login_user_1):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    
    create_public_channel(register_and_login_user_1)

    channel_info = dumps({
        'token': user_1_token,
        'channel_id': 1,
        'length': 500
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/standup/start',
        data = channel_info,
        headers = {'Content-Type': 'application/json'},
        method = 'POST'
    )

    payload = load(urllib.request.urlopen(req))

    channel_info = dumps({
        'token': user_1_token,
        'channel_id': 1,
        'length': 500
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/standup/start',
        data = channel_info,
        headers = {'Content-Type': 'application/json'},
        method = 'POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
'''