'''
HTTP Tests for auth/logout
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
def register_and_user_login_1_2():
    '''
    Registers and login a single user
    Fixture
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
    '''
    Basic working http tests for logout
    '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''

    logout_info = dumps({
        'token': user_1_token,

    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/logout',
        data=logout_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    payload = load(urllib.request.urlopen(req))
    assert payload['is_success']
