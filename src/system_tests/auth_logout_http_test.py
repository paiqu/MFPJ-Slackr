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
def register_login_aUser():
    
    # RESET
    req = urllib.request.Request(
        f'{BASE_URL}/workspace/reset',
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    register_info = dumps({
        'email': 'z5209488@unsw.edu.au',
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

    login_info = dumps({
        'email': 'z5209488@unsw.edu.au',
        'password': 'enigma'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    payload = load(urllib.request.urlopen(req))

    return payload


def logout_correct():
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_login_aUser

    login_info = dumps({
        'token': user_1_token
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/logout',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    payload = load(urllib.request.urlopen(req))

    assert payload == {'is_success' : True}

    global DATA
    users = DATA['users']
    user_1 = users[0]
    assert user_1.is_login == False


