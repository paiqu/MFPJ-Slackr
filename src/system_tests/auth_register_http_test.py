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

def test_basic():
    # Register a User 
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

    payload = load(urllib.request.urlopen(req))

    global DATA
    users = DATA['users']
    user_1 = users[0]

    assert user_1.email == 'alan@turing.com'
    assert user_1.password == 'enigma'
    assert user_1.name_first == 'Alan'
    assert user_1.name_last == 'Turing'


def invalid_email_test():
'''
Email entered is not a valid email 
'''
    # Register a User 
    register_info = dumps({
        #email is missing @ sign 
        'email': 'alanturing.com',
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
    
    with pytest.raises(InputError):
        load(urllib.request.urlopen(req))

def email_used_test():
    '''
    Email address is already being used by another user
    '''

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

    register_info2 = dumps({
        'email': 'alan@turing.com',
        'password': 'enigma',
        'name_first': 'Alan',
        'name_last': 'Turing'
    }).encode('utf-8')

    req2 = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(InputError):
        load(urllib.request.urlopen(req2))

def short_password_test():
    '''
    Password entered is less than 6 characters long
    '''

    register_info = dumps({
        'email': 'alan@turing.com',
        'password': 'chris',
        'name_first': 'Alan',
        'name_last': 'Turing'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(InputError):
        load(urllib.request.urlopen(req))

def short_fname_test():
    '''
    first name is too short
    name_first not is between 1 and 50 characters inclusive in length
    '''
    register_info = dumps({
        'email': 'alan@turing.com',
        'password': 'enigma',
        'name_first': '',
        'name_last': 'Turing'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(InputError):
        load(urllib.request.urlopen(req))

def long_fname_test():
    '''
    first name is too long 
    name_first not is between 1 and 50 characters inclusive in length
    '''
    register_info = dumps({
        'email': 'alan@turing.com',
        'password': 'enigma',
        'name_first': 'a'*51,
        'name_last': 'Turing'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(InputError):
        load(urllib.request.urlopen(req))
    
def short_lname_test():
    '''
    last name is too short
    name_first not is between 1 and 50 characters inclusive in length
    '''
    register_info = dumps({
        'email': 'alan@turing.com',
        'password': 'enigma',
        'name_first': 'Alan',
        'name_last': ''
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(InputError):
        load(urllib.request.urlopen(req))

def long_lname_test():
    '''
    last name is too long 
    name_first not is between 1 and 50 characters inclusive in length
    '''
    register_info = dumps({
        'email': 'alan@turing.com',
        'password': 'enigma',
        'name_first': 'Alan',
        'name_last': 'T'*51
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(InputError):
        load(urllib.request.urlopen(req))
    
