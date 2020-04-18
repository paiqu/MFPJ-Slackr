'''
This file is HTTP test for user/sethandle (PUT)

Parameter: (token, handle_str)
Return: {}

Always reset workspace when testing!!!!!!!!

Steps to test channel/create:
    1. Register a user
    2. The user login to the server
    3. the user set handle
    4. Time to Test:
        1. test for setting handle successfully
        2. test fot Error:
            Raise InputError when handle is between 2 and 20 characters
            Raise InputError when handle is already used by another user
'''
import sys
sys.path.append('..')
from json import load, dumps
import urllib.request
import pytest

PORT_NUMBER = '5204'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER
#BASE_URL now is 'http://127.0.0.1:5321'

@pytest.fixture
def register_and_login_user_1_2():
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

def test_set_handle(register_and_login_user_1_2):
    '''
    This function is for set handle successfully
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    # Set a handle
    user_info = dumps({
        'token': user_1_token,
        'handle': 'Tim'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/profile/sethandle',
        data=user_info,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    load(urllib.request.urlopen(req))

    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
    })
    payload = load(urllib.request.urlopen(f"{BASE_URL}/users/all?{queryString}"))

    assert payload['users'][0]['handle'] == 'Tim'

def test_error_short_type(register_and_login_user_1_2):
    '''
    This function is for test raising error if type short characters
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    # Set the user's handle
    user_info = dumps({
        'token': user_1_token,
        'handle': 'T'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/profile/sethandle',
        data=user_info,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_error_long_type(register_and_login_user_1_2):
    '''
    This function is for test raising error if type long name
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    # Set the user's handle
    user_info = dumps({
        'token': user_1_token,
        'handle': 'T' * 51
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/profile/sethandle',
        data=user_info,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_error_used_handle(register_and_login_user_1_2):
    '''
    This function is for test raising error if use used handle
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    # Set a user's handle
    user_info = dumps({
        'token': user_1_token,
        'handle': 'petepeteer',
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/profile/sethandle',
        data=user_info,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
