'''
This file is HTTP test for user/setemail (PUT)

Parameter: (token, email)
Return: {}

Always reset workspace when testing!!!!!!!!

Steps to test channel/create:
    1. Register a user
    2. The user login to the server
    3. the user set email
    4. Time to Test:
        1. test for setting email successfully
        2. test fot Error:
            Raise InputError when email is not valid
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

def test_set_email(register_and_login_user_1_2):
    '''
    This function is for set email successfully
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    # Set a email
    user_info = dumps({
        'token': user_1_token,
        'email': 'z3456789@unsw.edu.au'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/profile/setemail',
        data=user_info,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    load(urllib.request.urlopen(req))

    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
    })
    payload = load(urllib.request.urlopen(f"{BASE_URL}/users/all?{queryString}"))

    assert payload['users'][0]['email'] == 'z3456789@unsw.edu.au'

def test_error_invalid_type(register_and_login_user_1_2):
    '''
    This function is for test raising error if type invalid
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    # Set the user's email
    user_info = dumps({
        'token': user_1_token,
        'email': 'z3456789'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/profile/setemail',
        data=user_info,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_error_used_email(register_and_login_user_1_2):
    '''
    This function is for test raising error if use used email
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    # Set a user's email
    user_info = dumps({
        'token': user_1_token,
        'email': 'z7654321@unsw.edu.au'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/profile/setemail',
        data=user_info,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
