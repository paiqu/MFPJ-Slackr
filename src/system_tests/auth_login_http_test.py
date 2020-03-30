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
def register_a_user():
    register_info = dumps({
        'email': 'alan@turing.com',
        'password': 'enigma',
        'name_first': 'Alan',
        'name_last': 'Turing'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    payload = load(urllib.request.urlopen(req))

    return payload

def test_login_correct(register_a_user):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_a_user

    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token

    login_info = dumps({
        'email': 'alan@turing.com',
        'password': 'enigma'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    assert response['is_login'] == True

def invalid_email_test(register_a_user):
    '''
    Email entered is not a valid email using the method provided
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_a_user

    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token

    login_info = dumps({
        # Missing the @ symbol to test log in 
        'email': 'alanturing.com',
        'password': 'enigma'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with pytest.raises(InputError):
        load(urllib.request.urlopen(req))


def nonuser_email_test(register_a_user):
    '''
    Email entered does not belong to a user
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_a_user

    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token

    login_info = dumps({
        # Missing the @ symbol to test log in 
        'email': 'ada@lovelace.com',
        'password': 'enigma'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with pytest.raises(InputError):
        load(urllib.request.urlopen(req))

def incorrect_password_test(register_a_user):
    '''
    Password is not correct
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_a_user

    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token

    login_info = dumps({
        'email': 'alan@turing.com',
        'password': 'incorrectPassword'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with pytest.raises(InputError):
        load(urllib.request.urlopen(req))
