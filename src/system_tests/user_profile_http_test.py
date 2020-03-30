'''
This file is HTTP test for user/profile (GET)

Parameter: (token, u_id)
Return: {user}

Always reset workspace when testing!!!!!!!!

Steps to test user_profile:
    1. Register a user
    2. The user login to the server
    3. test
        1. return correct profile successfully
        2. test fot Error:
            Raise InputError when u_id is not a valid user
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

@pytest.fixture
def register_and_login_user_1():
    # RESET
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
    

def test_user_profile(register_and_login_user_1):

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1
    
    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token

    # Get user profile
    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'u_id' : 1
    })
    payload = load(urllib.request.urlopen(f"{BASE_URL}/user/profile?{queryString}"))
    
    assert payload[0]['u_id'] == 1
    assert payload[0]['email'] == 'z5237609@unsw.edu.au'
    assert payload[0]['name_first'] == 'Xinlei'   
    assert payload[0]['name_last'] == 'Zhang'
    #assert payload[0]['handle_str'] == 'zhangxinlei'

def test_user_profile_inputerror(register_and_login_user_1):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1
    
    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token


    # Create a private channel
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

    payload = load(urllib.request.urlopen(req))
    
    assert payload['channel_id'] == 1


def test_error_long_name(register_and_login_user_1):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1
    
    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token


    # Create a public channel
    channel_info = dumps({
        'token': user_1_token,
        'name': 'ihaveasupersuperlongnamethatislongerthan20chars',
        'is_public': True
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channels/create',
        data=channel_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    # with pytest.raises(InputError):
    #     load(urllib.request.urlopen(req))
    
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)


        
