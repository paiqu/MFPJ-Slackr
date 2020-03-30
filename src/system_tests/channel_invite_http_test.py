import sys
sys.path.append('..')
from json import load, dumps
import urllib.request
import urllib.parse
import pytest
from data import DATA
from error import InputError
import requests


PORT_NUMBER = '5321'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER
#BASE_URL now is 'http://127.0.0.1:5321'

@pytest.fixture
def register_login_aUser():
    register_info = dumps({
        'email': 'alan@turing.com',
        'password': 'enigma',
        'name_first': 'Alan',
        'name_last': 'Turing'
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
# This will return correct 
def test_invite_basic(register_and_login_user_1_and_2):
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

    # user_2 join user_1's channel
    join_info = dumps({
        'token': user_1_token,
        'channel_id': 1
        'u_id': 2
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/invite',
        data=join_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    payload = load(urllib.request.urlopen(req))
    assert payload == {}


def invalid_channelId_test(register_and_login_user_1_and_2):
    '''
    channel_id does not refer to a valid channel that the authorised user is part of.
    '''
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

    # user_1 invites user_2 
    join_info = dumps({
        'token': user_1_token,
        'channel_id': 50
        'u_id': 2
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/invite',
        data=join_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)


def invalid_userID_test(register_and_login_user_1_and_2):
    '''
    u_id does not refer to a valid user
    '''

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''
    
    # user_1 creates a public channel
    channel_info = dumps({
        'token': user_1_token,
        'name': 'a channel',
        'is_public': False
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channels/create',
        data=channel_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    # user_2 join user_1's channel
    join_info = dumps({
        'token': user_1_token,
        'channel_id': 1
        'u_id': 20 
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/invite',
        data=join_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )


    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def invalid_channelId_test(register_and_login_user_1_and_2):
    '''
    channel_id does not refer to a valid channel that the authorised user is part of.
    '''
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

    # user_1 invites user_2 
    join_info = dumps({
        'token': user_1_token,
        'channel_id': 50
        'u_id': 2
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/invite',
        data=join_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)


def access_error_test(register_and_login_user_1_and_2):
    '''
    the authorised user is not already a member of the channel
    '''

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''
    
    # user_1 creates a public channel
    channel_info = dumps({
        'token': user_1_token,
        'name': 'a channel',
        'is_public': False
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channels/create',
        data=channel_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    # user_2 join user_1's channel
    join_info = dumps({
        'token': user_2_token,
        'channel_id': 1
        'u_id': 1
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/invite',
        data=join_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
