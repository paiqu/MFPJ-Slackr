'''
This file is HTTP test for user/all (GET)

Parameter: (token)
Return: {users}

Always reset workspace when testing!!!!!!!!

Steps to test channel/create:
    1. Register a user
    2. The user login to the server
    3. the user set handle
    4. Time to Test:
        1. test for return users all successfully
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

def test_return_one_usersall(register_and_login_user_1):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1
    
    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token


    # Set a handle
    user_info = dumps({
        'token': user_1_token
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/all',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'GET'
    )

    payload = load(urllib.request.urlopen(req))

    global DATA
    users = DATA['users']
    user_one = users[0]
    assert user_one.u_id == 1
    assert user_one.email == 'z1234567@unsw.edu.au'
    assert user_one.name_first == 'Xinlei'
    assert user_one.name_last == 'Matthew'
    assert user_one.handle_str == 'xinleimatthew'

def test_two_users_all(register_and_login_user_1, register_and_login_user_2):
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


    # Set a user's info
    user_info = dumps({
        'token': user_1_token,
    }).encode('utf-8')

    req_one = urllib.request.Request(
        f'{BASE_URL}/user/all',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'GET'
    )

    user_info = dumps({
        'token': user_2_token,
    }).encode('utf-8')

    req_two = urllib.request.Request(
        f'{BASE_URL}/user/all',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'GET'
    )

    payload = load(urllib.request.urlopen(req))

    global DATA
    users = DATA['users']
    user_one = users[0]
    user_two = users[1]
    assert user_one.u_id == 1
    assert user_one.email == 'z1234567@unsw.edu.au'
    assert user_one.name_first == 'Xinlei'
    assert user_one.name_last == 'Matthew'
    assert user_one.handle_str == 'xinleimatthew'

    assert user_two.u_id == 2
    assert user_two.email == 'z2345678@unsw.edu.au'
    assert user_two.name_first == 'Haofu'
    assert user_two.name_last == 'Adam'
    assert user_two.handle_str == 'haofuadam'

    