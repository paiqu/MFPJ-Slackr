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
import time
import datetime
from datetime import timezone
import sys
sys.path.append('..')
from json import load, dumps
import urllib
import flask
import pytest
from data import *
from error import InputError


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

    payload = load(urllib.request.urlopen(req))
    return payload
    
def create_public_channel(register_and_login_user_1):

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

def test_standup_start(register_and_login_user_1):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    create_public_channel(register_and_login_user_1)

    # Set a first and last name
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

    channels = DATA['channels']
    standups = DATA['standups']
    for channel in channels:
        if channel['channel_id'] == channel_id:
            assert channel['is_standup_active'] == True
            for standup in standups:
                if standup['channel_id'] == channel_id:
                    assert time_end == standup['time_end']
    payload = load(urllib.request.urlopen(req))


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