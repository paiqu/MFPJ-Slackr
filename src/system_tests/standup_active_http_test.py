'''
This file is HTTP test for standup/active (GET)

Parameter: (token, channel_id)
Return: {is_active, time_finish}

Always reset workspace when testing!!!!!!!!

Steps to test standup/start:
    1. Register a user
    2. The user login to the server
    3. the user create a channel
    4. Time to Test:
        1. test for returning is_active and time_end successfully
        2. test fot Error:
            Raise InputError when channel_id is not valid
'''
import datetime
from datetime import timezone
import sys
sys.path.append('..')
from json import load, dumps
import urllib.request
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
    '''
    create a public channel
    '''
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
    return payload

def test_standup_active(register_and_login_user_1):
    '''
    This function is to test when channel1 is standup.
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

    payload = load(urllib.request.urlopen(req))

    length = 500
    now = datetime.datetime.utcnow()
    time_start = int(now.replace(tzinfo=timezone.utc).timestamp())
    time_end = int(time_start + int(length))
    assert payload == time_end

    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'channel_id' : 1
    })
    payload = load(urllib.request.urlopen(f"{BASE_URL}/standup/active?{queryString}"))

    assert payload['is_active'] == True

def test_standup_active_2(register_and_login_user_1):
    '''
    This function is to test when channel2 is not standup.
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

    payload = load(urllib.request.urlopen(req))


    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'channel_id' : 2
    })
    payload = load(urllib.request.urlopen(f"{BASE_URL}/standup/active?{queryString}"))

    assert payload['is_active'] == False
    assert payload['time_finish'] == None

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
