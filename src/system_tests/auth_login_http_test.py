'''
This file is HTTP test for auth/login (POST)
'''
import sys
sys.path.append('..')
from json import load, dumps
import urllib.request
import urllib.parse
import pytest
#from data import DATA


PORT_NUMBER = '5444'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER

@pytest.fixture
def register_and_user_1_2():
    '''
    Fixture to Register one users
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

def test_login_basic(register_and_user_1_2):
    '''
    A functioning basic HTTP test
    '''

    login_info = dumps({
        'email': 'z1234567@unsw.edu.au',
        'password': 'thisisaPassword',
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    payload = load(urllib.request.urlopen(req))
    assert payload['u_id'] == 1
    assert payload['token'] == 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

def test_invalid_email(register_and_user_1_2):
    '''
    Email entered is not a valid email using the method provided
    '''
    login_info = dumps({
        # Missing the @ symbol to test log in
        'email': 'z1234567unsw.edu.au',
        'password': 'thisisaPassword',
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)


def test_nonuser_email(register_and_user_1_2):
    '''
    Email entered does not belong to a user
    '''
    login_info = dumps({
        # Missing the @ symbol to test log in
        'email': 'z5209488@unsw.edu.a',
        'password': 'enigma'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)


def test_incorrect_password(register_and_user_1_2):
    '''
    Password is not correct
    '''
    login_info = dumps({
        'email': 'z5209488@unsw.edu.au',
        'password': 'incorrectPassword'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/login',
        data=login_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
