import sys
sys.path.append('..')
from json import load, dumps
import urllib.request
import urllib.parse
import pytest
from data import DATA
from error import InputError
import requests


PORT_NUMBER = '5444'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER
#BASE_URL now is 'http://127.0.0.1:5321'

@pytest.fixture
def register_loginx2_create_invite():
    # RESET
    req = urllib.request.Request(
        f'{BASE_URL}/workspace/reset',
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    # REGISTER user_1
    register_info_1 = dumps({
        'email': 'z5209488@unsw.edu.au',
        'password': 'enigma',
        'name_first': 'Alan',
        'name_last': 'Turing'
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
        'email': 'z5432455@unsw.edu.au',
        'password': 'lovepassword',
        'name_first': 'Ada',
        'name_last': 'Lovelace'
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
        'email': 'z5209488@unsw.edu.au',
        'password': 'enigma'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    # Login user_2
    login_info = dumps({
        'email': 'z5432455@unsw.edu.au',
        'password': 'lovepassword'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))
    #return payload

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
        'channel_id': 1,
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
def test_details_basic(register_loginx2_create_invite):
    '''
    This test should pass with no issues
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    #user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''

    #Requests channel details

    queryString = urllib.parse.urlencode({
        'token': user_1_token,
        'channel_id': 1,
    })
    payload = load(urllib.request.urlopen(f"{BASE_URL}/channel/details?{queryString}"))

    '''
    req = urllib.request.Request(
        f'{BASE_URL}/channel/details',
        data=channel_details,
        headers={'Content-Type': 'application/json'},
        method='GET'
    )

    payload = load(urllib.request.urlopen(req))
    '''
    assert payload['name'] == 'a channel'
    assert payload['owner_members'] == [{"u_id": 1, "name_first": "Alan", "name_last": "Turing"}]

def test_invalid_channelID(register_loginx2_create_invite):
    '''
    Channel ID is not a valid channel
    '''

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''

    #Requests channel details
    channel_details = dumps({
        'token': user_1_token,
        'channel_id': 50,
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/details',
        data=channel_details,
        headers={'Content-Type': 'application/json'},
        method='GET'
    )
    '''
    payload = load(urllib.request.urlopen(req))
    '''
    with pytest.raises(urllib.error.HTTPError):
        
        load(urllib.request.urlopen(req))
        #urllib.request.urlopen(req)
        
def test_unauthorised_user(register_loginx2_create_invite):
    '''
    Authorised user is not a member of channel with channel_id
    '''

    register_info_2 = dumps({
        'email': 'z5454545@unsw.edu.au',
        'password': 'testPassword',
        'name_first': 'Test',
        'name_last': 'User'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info_2,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    login3_info = dumps({
        'email': 'z5454545@unsw.edu.au',
        'password': 'testPassword'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login3_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    user_3_token= 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMyJ9.hnzKv5QKl78L2jWvtB8w9kcxZHo1UFxGN5shF7HBK0Y\''


    #Requests channel details
    channel_details = dumps({
        'token': user_3_token,
        'channel_id': 1,
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/details',
        data=channel_details,
        headers={'Content-Type': 'application/json'},
        method='GET'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)