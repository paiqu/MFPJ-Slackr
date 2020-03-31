'''
This file is HTTP test for message_pin (POST)

Parameter: (token, message_id)
Return: {}

Steps to test message_pin:
    1. Register a user
    2. The user login to the server
    3. create a channel
    4. send a message and pin it
    5. test
        1. pin message successfully
        2. test fot Error:
            Raise InputError when message is more than 1000 characters
            The authorised user has not joined the channel they are trying to post to
'''
import sys
sys.path.append('..')
from json import load, dumps
import urllib.request
import urllib.parse
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
def register_and_login_user_2():

    # REGISTER
    register_info = dumps({
        'email': 'z1234567@unsw.edu.au',
        'password': 'Xinleizhang2017',
        'name_first': 'Matty',
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
        'email': 'z1234567@unsw.edu.au',
        'password': 'Xinleizhang2017'
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
    payload = load(urllib.request.urlopen(req))
    return payload

def test_message_pin_inputerror1(register_and_login_user_1, create_public_channel, send_a_message):

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1

    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token

    response2 = create_public_channel
    assert response2['channel_id'] == 1

    response3 = send_a_message
    assert response3['message_id'] == 1

    message_info = dumps({
        'token': user_1_token,
        'message_id': 2
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/message/pin',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_message_pin_inputerror2(register_and_login_user_1, create_public_channel, send_a_message):

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1

    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token

    response2 = create_public_channel
    assert response2['channel_id'] == 1

    response3 = send_a_message
    assert response3['message_id'] == 1

    message_info = dumps({
        'token': user_1_token,
        'message_id': 1
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/message/pin',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    load(urllib.request.urlopen(req))

    message_info2 = dumps({
        'token': user_1_token,
        'message_id': 1
    }).encode('utf-8')

    req2 = urllib.request.Request(
        f'{BASE_URL}/message/pin',
        data=message_info2,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req2)

def test_message_pin_inputerror3(register_and_login_user_1, create_public_channel, send_a_message, register_and_login_user_2):

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''
    response = register_and_login_user_1

    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token

    response2 = create_public_channel
    assert response2['channel_id'] == 1

    response3 = send_a_message
    assert response3['message_id'] == 1

    response4 = register_and_login_user_2
    assert response4['u_id'] == 2
    assert isinstance(response4['token'], str)
    assert response4['token'] == user_2_token

    # user2 join the channel
    join_info = dumps({
        'token': user_2_token,
        'channel_id': 1
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/channel/join',
        data=join_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    load(urllib.request.urlopen(req))

    # user 2 pin a message
    message_info = dumps({
        'token': user_2_token,
        'message_id': 1
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/message/pin',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_message_pin_accesserror(register_and_login_user_1, create_public_channel, send_a_message, register_and_login_user_2):

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    user_2_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMiJ9.UNGv0HfSeyM4FtXkAc4HfuOl_HyNLFmRMeLx_4c0Ryg\''
    response = register_and_login_user_1

    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token

    response2 = create_public_channel
    assert response2['channel_id'] == 1

    response3 = send_a_message
    assert response3['message_id'] == 1

    response4 = register_and_login_user_2
    assert response4['u_id'] == 2
    assert isinstance(response4['token'], str)
    assert response4['token'] == user_2_token

    # user 2 pin a message
    message_info = dumps({
        'token': user_2_token,
        'message_id': 1
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/message/pin',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_message_pin(register_and_login_user_1, create_public_channel, send_a_message):

    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    response = register_and_login_user_1

    assert response['u_id'] == 1
    assert isinstance(response['token'], str)
    assert response['token'] == user_1_token

    response2 = create_public_channel
    assert response2['channel_id'] == 1

    response3 = send_a_message
    assert response3['message_id'] == 1

    message_info = dumps({
        'token': user_1_token,
        'message_id': 1
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/message/pin',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    load(urllib.request.urlopen(req))

    # Get search
    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'query_str' : 'hello'
    })
    payload = load(urllib.request.urlopen(f"{BASE_URL}/search?{queryString}"))

    assert len(payload['messages']) == 1
    assert payload['messages'][0]['is_pinned'] == True
