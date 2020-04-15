'''
This file is HTTP test for message/unreact (POST)

Parameter: (token, message_id, react_id)
Return: {}

Always reset workspace when testing!!!!!!!!

Steps to test channel/leave:
    1. Register user_1, login and create channel 
    2. send user_1 send messages 
    3. Time to Test:
        1. test for react a message
        2. Input Error:
            -invalid message_id
            -invalid react_id
            -message not been reacted with react_id
'''


import sys
sys.path.append('..')
from json import load, dumps
import urllib.request
import urllib.parse
import pytest


PORT_NUMBER = '1231'
BASE_URL = 'http://127.0.0.1:' + PORT_NUMBER

@pytest.fixture
def register_and_login_user_1():
    # RESET
    req = urllib.request.Request(
        f'{BASE_URL}/workspace/reset',
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    # REGISTER
    register_info = dumps({
        'email': 'z1234567@unsw.edu.au',
        'password': 'thisisaPassword',
        'name_first': 'Peter',
        'name_last': 'Parker'
    }).encode('utf-8')


    req = urllib.request.Request(
        f'{BASE_URL}/auth/register',
        data=register_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))
    
    # Login
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
    
@pytest.fixture
def create_public_channel():
    # Create public channel 

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    channel_info = dumps({
        'token': user_1_token,
        'name': 'publicchannel',
        'is_public': True
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channels/create',
        data=channel_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    payload = load(urllib.request.urlopen(req))
    return payload

@pytest.fixture
def send_messages():
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    
    # send message
    message_info = dumps({
        'token': user_1_token,
        'channel_id': 1,
        'message': 'hello'
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f'{BASE_URL}/message/send',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    load(urllib.request.urlopen(req))
    return

@pytest.fixture
def message_react():
    
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    message_info = dumps({
        'token': user_1_token,
        'message_id': 1,
        'react_id': 1
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f'{BASE_URL}/message/react',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    load(urllib.request.urlopen(req))
    return

def test_message_unreact(register_and_login_user_1, create_public_channel, send_messages, message_react):
    
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    message_info = dumps({
        'token': user_1_token,
        'message_id': 1,
        'react_id': 1
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f'{BASE_URL}/message/unreact',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    load(urllib.request.urlopen(req))
    
    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'query_str' : 'hello'
    })
    mess_info = load(urllib.request.urlopen(f"{BASE_URL}/search?{queryString}"))

    
    assert mess_info['messages'][0]['message_id'] == 1
    assert len(mess_info['messages'][0]['reacts']) == 0
    
def test_invalid_message_id(register_and_login_user_1, create_public_channel, send_messages, message_react):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    message_info = dumps({
        'token': user_1_token,
        'message_id': 123123123,
        'react_id': 1
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f'{BASE_URL}/message/unreact',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_invalid_react_id(register_and_login_user_1, create_public_channel, send_messages, message_react):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    message_info = dumps({
        'token': user_1_token,
        'message_id': 1,
        'react_id': 123123
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f'{BASE_URL}/message/unreact',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
        
def test_not_exist_react_id_with_message(register_and_login_user_1, create_public_channel, send_messages):
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    message_info = dumps({
        'token': user_1_token,
        'message_id': 1,
        'react_id': 1
    }).encode('utf-8')
    
    req = urllib.request.Request(
        f'{BASE_URL}/message/unreact',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
    
