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
from json import load, dumps
import urllib.request
import urllib.parse
import sys
sys.path.append('..')
import pytest

PORT_NUMBER = '5204'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER

@pytest.fixture
def register_and_login_user_1():
    '''
    fixture for register login
    '''
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
    '''
    test the normal case
    '''
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

    assert payload['user']['u_id'] == 1
    assert payload['user']['email'] == 'z5237609@unsw.edu.au'
    assert payload['user']['name_first'] == 'Xinlei'
    assert payload['user']['name_last'] == 'Zhang'
    assert payload['user']['handle_str'] == 'xinleizhang'

def test_user_profile_inputerror(register_and_login_user_1):
    '''
    test the inputerror
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1

    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token

    # Get user profile
    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'u_id' : 2
    })

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{BASE_URL}/user/profile?{queryString}")
