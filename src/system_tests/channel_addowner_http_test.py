'''
Steps to test channel/owner:
    1. register and login two users: user_1 and user_2
    2. user_1 creates a channel
    3. Test:
        1. user_1 add user_2 as a owner
        2. Input Error:
            1. invalid channel id
            2. user_1 add itself as an owner
        3. Access Error:
            1. when owner is not an owner of slakr,
                or an owner of this channel.
'''

import sys
sys.path.append('..')
from json import load, dumps
import urllib.request
import urllib.parse
import pytest
from data import DATA

PORT_NUMBER = '5204'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER
#BASE_URL now is 'http://127.0.0.1:5321'

@pytest.fixture
def register_and_login_user_1_and_2():
    # RESET
    req = urllib.request.Request(
        f'{BASE_URL}/workspace/reset',
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    # REGISTER user_1
    register_info_1 = dumps({
        'email': 'z1234567@unsw.edu.au',
        'password': 'thisisaPassword',
        'name_first': 'Peter',
        'name_last': 'Parker'
    }).encode('utf-8')


    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info_1,
        headers={'Content-Type': 'application/json'},
        method='POST'
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
    
    # Login user_1
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
    #return payload

def test_add_user_2_as_owner(register_and_login_user_1_and_2):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''
    
    # user_1 creates a public channel
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

    load(urllib.request.urlopen(req))

    # user_1 add user_2 as an owner
    addowner_info = dumps({
        'token': user_1_token,
        'channel_id': 1,
        'u_id': 2
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/addowner',
        data=addowner_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    payload = load(urllib.request.urlopen(req))
    assert payload == {}

def test_invalid_channel_id(register_and_login_user_1_and_2):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''
    
    # user_1 creates a public channel
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

    load(urllib.request.urlopen(req))

    # user_1 add user_2 as an owner
    addowner_info = dumps({
        'token': user_1_token,
        'channel_id': 40,
        'u_id': 2
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/addowner',
        data=addowner_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_already_owner(register_and_login_user_1_and_2):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''
    
    # user_1 creates a public channel
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

    load(urllib.request.urlopen(req))

    # user_1 add user_2 as an owner
    addowner_info = dumps({
        'token': user_1_token,
        'channel_id': 1,
        'u_id': 1
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/addowner',
        data=addowner_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    
def test_access_error(register_and_login_user_1_and_2):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''
    
    # user_1 creates a public channel
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

    load(urllib.request.urlopen(req))

    # user_1 add user_2 as an owner
    addowner_info = dumps({
        'token': user_2_token,
        'channel_id': 1,
        'u_id': 2
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/addowner',
        data=addowner_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)