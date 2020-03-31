'''
This file is HTTP test for search (GET)

Parameter: (token, query_str)
Return: {messages}

Steps to test search:
    1. Register a user
    2. The user login to the server
    3. create a channel
    4. send a message and search
    5. test
        1. search successfully
'''

from json import load, dumps
import urllib.request
import urllib.parse
import sys
sys.path.append('..')
import pytest

PORT_NUMBER = '5204'
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
        'email': 'z5237609@unsw.edu.au',
        'password': 'Zxl010128',
        'name_first': 'Xinlei',
        'name_last': 'Zhang'
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
        'email': 'z5237609@unsw.edu.au',
        'password': 'Zxl010128'
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
def create_private_channel():
    # Create public channel

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    channel_info = dumps({
        'token': user_1_token,
        'name': 'privatechannel',
        'is_public': False
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
def send_a_message():
    # send a message

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
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

    message_info = dumps({
        'token': user_1_token,
        'channel_id': 2,
        'message': 'helloworld'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/message/send',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    payload = load(urllib.request.urlopen(req))
    return payload

def test_search(register_and_login_user_1, create_public_channel, create_private_channel, send_a_message):

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1

    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token

    response2 = create_public_channel
    assert response2['channel_id'] == 1

    response3 = create_private_channel
    assert response3['channel_id'] == 2

    response4 = send_a_message
    assert response4['message_id'] == 2

    # Get search
    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'query_str' : 'hel'
    })
    payload = load(urllib.request.urlopen(f"{BASE_URL}/search?{queryString}"))

    assert len(payload['messages']) == 2
    assert payload['messages'][0]['message'] == 'helloworld'
    assert payload['messages'][1]['message'] == 'hello'
