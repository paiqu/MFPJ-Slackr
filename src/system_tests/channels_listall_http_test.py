'''
This file is HTTP test for channels/listall (GET)

Parameter: (token)
Return: {channels}

Always reset workspace when testing!!!!!!!!

Steps to test channels/list:
    1. Register user_1 and user_2
    2. The user_1 and user_2 login to the server
    3. the user_1 and user_2 create channels separately
    4. Time to Test:
        1. test for only list channel that create by user_1
'''
import sys
sys.path.append('..')
from json import load, dumps
import urllib.request
import urllib.parse
import pytest

PORT_NUMBER = '1231'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER

@pytest.fixture
def register_and_login_user_1():
    '''set up user'''
    req = urllib.request.Request(
        f'{BASE_URL}/workspace/reset',
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))
    # REGISTER
    register_info = dumps({
        'email': 'z5237609@unsw.edu.au',
        'password': 'Zxl010128',
        'name_first': 'Xinlei',
        'name_last': 'Zhang'
    }).encode('utf-8')


    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    # Login
    login_info = dumps({
        'email': 'z5237609@unsw.edu.au',
        'password': 'Zxl010128'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    payload = load(urllib.request.urlopen(req))
    return payload

@pytest.fixture
def register_and_login_user_2():
    '''REGISTER'''
    register_info = dumps({
        'email': 'z1234567@unsw.edu.au',
        'password': 'Zxl010128',
        'name_first': 'fir',
        'name_last': 'fox'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    # Login
    login_info = dumps({
        'email': 'z5237609@unsw.edu.au',
        'password': 'Zxl010128'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    payload = load(urllib.request.urlopen(req))
    return payload

@pytest.fixture
def create_public_channel():
    '''Create public channel'''

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    channel_info = dumps({
        'token': user_1_token,
        'name': 'publicchannel',
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

@pytest.fixture
def create_public_channel_2():
    '''Create public channel'''

    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''
    channel_info = dumps({
        'token': user_2_token,
        'name': 'channel_2',
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

def test_only_one_channel(register_and_login_user_1, create_public_channel):
    '''create one channel'''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
    })

    payload = load(urllib.request.urlopen(f"{BASE_URL}/channels/listall?{queryString}"))
    assert payload['channels'][0]['channel_id'] == 1
    assert payload['channels'][0]['name'] == 'publicchannel'

def test_two_channels_created_by_diff_users(register_and_login_user_1, create_public_channel, register_and_login_user_2, create_public_channel_2):
    '''test two channels created by diff users'''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
    })

    payload = load(urllib.request.urlopen(f"{BASE_URL}/channels/listall?{queryString}"))
    assert payload['channels'][0]['channel_id'] == 1
    assert payload['channels'][0]['name'] == 'publicchannel'
    assert payload['channels'][1]['channel_id'] == 2
    assert payload['channels'][1]['name'] == 'channel_2'
