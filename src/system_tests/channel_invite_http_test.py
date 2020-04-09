'''
HTTP Tests for Channel/invite
'''
import sys
sys.path.append('..')
from json import load, dumps
import urllib
#import flask
import pytest
#from data import *
#from error import InputError, AccessError


PORT_NUMBER = '5444'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER
#BASE_URL now is 'http://127.0.0.1:5321'

@pytest.fixture
def register_and_login_user_1():
    '''
    Fixture to Register and Login User
    '''
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
        data=register_info,
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
    '''
    Create a public channel
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

    load(urllib.request.urlopen(req))

def test_channel_invite_basic(register_and_login_user_1):
    '''
    Passing HTTP Test
    When all passes
    '''
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
        data=channel_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    payload = load(urllib.request.urlopen(req))
    assert payload == {}

def test_invalid_channelId(register_and_login_user_1):
    '''
    channel_id does not refer to a valid channel that the authorised user is part of.
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    #user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''

    create_public_channel(register_and_login_user_1)

    # user_1 invites user_2
    invite_info = dumps({
        'token': user_1_token,
        'channel_id': 50,
        'u_id': 2
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/invite',
        data=invite_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)



def test_invalid_userID(register_and_login_user_1):
    '''
    u_id does not refer to a valid user
    '''

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    #user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''

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
        'channel_id': 1,
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


def test_invalid_userAuthorise(register_and_login_user_1):
    '''
    the authorised user is not already a member of the channel
    '''

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''

    # user_2 creates a public channel
    channel_info = dumps({
        'token': user_2_token,
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
        'channel_id': 1,
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
