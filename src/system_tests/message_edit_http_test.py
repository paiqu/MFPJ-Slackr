'''
This file is HTTP test for message/edit (PUT)

Parameter: (token, message_id, message)
Return: {}

Always reset workspace when testing!!!!!!!!

Steps to test channels/list:
    1. setup user_1, channel and send message
    2. Time to Test:
        1. test update message with new texts
        2. update with empty string, which will delete the msg
        3. AccessError
            - Message with message_id was sent by the authorised user making this request
            - The authorised user is an owner of this channel or the slackr
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
    '''set up user'''
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
    '''Create public channel'''

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
    '''function for send message'''
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
    return {}

def test_update_message(register_and_login_user_1, create_public_channel, send_messages):
    '''test for update message'''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    message_info = dumps({
        'token': user_1_token,
        'message_id': 1,
        'message': 'been changed'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/message/edit',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    load(urllib.request.urlopen(req))

    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'channel_id' : 1,
        'start': 0,
    })

    payload = load(urllib.request.urlopen(f"{BASE_URL}/channel/messages?{queryString}"))

    assert payload['messages'][0]['message'] == 'been changed'
    assert payload['messages'][0]['message_id'] == 1

def test_blank_message(register_and_login_user_1, create_public_channel, send_messages):
    '''test for update blank message'''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    message_info = dumps({
        'token': user_1_token,
        'message_id': 1,
        'message': ''
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/message/edit',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    load(urllib.request.urlopen(req))

    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'channel_id' : 1,
        'start': 0,
    })

    payload = load(urllib.request.urlopen(f"{BASE_URL}/channel/messages?{queryString}"))
    assert len(payload['messages']) == 0
def test_unauthorised_user_try_to_edit(register_and_login_user_1, create_public_channel, send_messages):
    '''
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an owner of this channel or the slackr
    '''
    user_1_token = 'this is not a valid token'
    message_info = dumps({
        'token': user_1_token,
        'message_id': 1,
        'message': ''
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{BASE_URL}/message/edit',
        data=message_info,
        headers={'Content-Type': 'application/json'},
        method='PUT'
    )
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
