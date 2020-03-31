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


PORT_NUMBER = '5321'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER

@pytest.fixture
def register_and_user_login_1_2():
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

    load(urllib.request.urlopen(req))


def test_logout_basic(register_and_user_login_1_2):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    
    logout_info = dumps({
        'token': user_1_token,

    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/logout',
        data = logout_info,
        headers = {'Content-Type': 'application/json'},
        method = 'POST'
    )
    payload = load(urllib.request.urlopen(req))
    assert payload['is_success'] == True
    