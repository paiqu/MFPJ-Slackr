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
import urllib.parse
import pytest
from data import DATA
from error import InputError
import requests

PORT_NUMBER = '5321'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER
#BASE_URL now is 'http://127.0.0.1:5321'

@pytest.fixture
def register_and_login_user_1():
    register_info = dumps({
        'email': 'z1234567@unsw.edu.au',
        'password': 'thisisaPassword',
        'name_first': 'Xinlei',
        'name_last': 'Matthew'
    }).encodee('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data = register_info,
        headers = {'Content-Type': 'application/json'},
        method = 'POST'
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

def register_and_login_user_2():
    register_info = dumps({
        'email': 'z2345678@unsw.edu.au',
        'password': 'thisisPassword2',
        'name_first': 'Haofu',
        'name_last': 'Adam'
    }).encodee('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data = register_info,
        headers = {'Content-Type': 'application/json'},
        method = 'POST'
    )

    load(urllib.request.urlopen(req))
    
    login_info = dumps({
        'email': 'z2345678@unsw.edu.au',
        'password': 'thisisPassword2'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data = login_info,
        headers = {'Content-Type': 'application/json'},
        method = 'POST'
    )

    payload = load(urllib.request.urlopen(req))
    return payload  

def test_set_handle(register_and_login_user_1):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1
    
    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token


    # Set a handle
    user_info = dumps({
        'token': user_1_token,
        'handle_str': 'MFPJ',
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/sethandle',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'PUT'
    )

    payload = load(urllib.request.urlopen(req))

    global DATA
    users = DATA['users']
    user_one = users[0]
    assert user_one.handle_str == 'MFPJ'

def test_error_short_handle(register_and_login_user_1):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1
    
    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token


    # Set handle
    user_info = dumps({
        'token': user_1_token,
        'handle_str': 'M',
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/sethandle',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'PUT'
    )

    with pytest.raises(InputError):
        load(urllib.request.urlopen(req))

def test_error_long_handle(register_and_login_user_1):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1
    
    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token


    # Set handle
    user_info = dumps({
        'token': user_1_token,
        'handle_str': 'M' * 23,
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/sethandle',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'PUT'
    )

    with pytest.raises(InputError):
        load(urllib.request.urlopen(req))

def test_error_used_handle(register_and_login_user_1, register_and_login_user_2):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''
    response_2 = register_and_login_user_2

    assert response['u_id'] == 1
    assert response_2['u_id'] == 2
    assert isinstance(response['token'], str)
    assert isinstance(response_2['token'], str)
    assert response['token'] == user_1_token
    assert response_2['token'] == user_2_token


    # Set a user's handle
    user_info = dumps({
        'token': user_1_token,
        'handle': 'haofuadam'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/sethandle',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'PUT'
    )

    with pytest.raises(InputError):
        load(urllib.request.urlopen(req))