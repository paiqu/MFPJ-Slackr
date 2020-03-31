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
import urllib
import flask
import pytest
from data import *
from error import InputError



PORT_NUMBER = '5321'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER
#BASE_URL now is 'http://127.0.0.1:5321'

@pytest.fixture
def register_and_login_user_1_2():
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
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1_2
    
    # Set a email
    user_info = dumps({
        'token': user_1_token,
        'handle': 'Tim'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/sethandle',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'PUT'
    )
    for user in DATA['users']:
        if user['u_id'] == token_to_uid(token):
            assert user['handle'] == 'Tim'
    payload = load(urllib.request.urlopen(req))
    assert payload == {}

def test_error_short_type(register_and_login_user_1_2):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    # Set the user's handle
    user_info = dumps({
        'token': user_1_token,
        'handle': 'T'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/sethandle',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'PUT'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_error_long_type(register_and_login_user_1_2):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    # Set the user's handle
    user_info = dumps({
        'token': user_1_token,
        'handle': 'T' * 51
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/sethandle',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'PUT'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_error_used_email(register_and_login_user_1_2):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1_2
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''
    response_2 = register_and_login_user_1_2
    
    # Set a user's handle
    user_info = dumps({
        'token': user_1_token,
        'handle': 'petepeteer',\
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/sethandle',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'PUT'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)