'''
This file is HTTP test for user/setname (PUT)

Parameter: (token, name_first, name_last)
Return: {}

Always reset workspace when testing!!!!!!!!

Steps to test channel/create:
    1. Register a user
    2. The user login to the server
    3. the user set first name and last name (public or private)
    4. Time to Test:
        1. test for firstname and lastname successfully
        2. test fot Error:
            Raise InputError when name is not between 1 and 50 characters
'''
import sys
sys.path.append('..')
from json import load, dumps
import urllib
import flask
import pytest
from data import DATA
from error import InputError



PORT_NUMBER = '5321'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER
#BASE_URL now is 'http://127.0.0.1:5321'

@pytest.fixture
def register_and_login_user_1():
    # RESET
    req = urllib.request.Request(
        f'{BASE_URL}/workspace/reset',
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))
    
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
    

def test_set_name(register_and_login_user_1):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1
    
    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token


    # Set a first and last name
    user_info = dumps({
        'token': user_1_token,
        'name_first': 'Zane',
        'name_last': 'James'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/setname',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'PUT'
    )
    
    payload = load(urllib.request.urlopen(req))
    users = DATA['users']
    assert users[0]['name_first'] == 'Zane'
    assert users[0]['name_last'] == 'James'

def test_error_no_type(register_and_login_user_1):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1
    
    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token


    # Set the user's first and last name
    user_info = dumps({
        'token': user_1_token,
        'name_first': '',
        'name_last': ''
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/setname',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'PUT'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_error_long_name(register_and_login_user_1):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1
    
    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token


    # Set a user's name first and last
    user_info = dumps({
        'token': user_1_token,
        'name_first': 'ihavea' * 51,
        'name_last': 'fhsgdyw' * 51
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/user/setname',
        data = user_info,
        headers = {'Content-Type': 'application/json'},
        method = 'PUT'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
