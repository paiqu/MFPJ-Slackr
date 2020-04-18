'''
This file is HTTP test for channel/messages (GET)

Parameter: (token, channel_id, start)
Return: {messages, start, end}
Always reset workspace when testing!!!!!!!!
Steps to test channels/list:
    1. Register user_1
    2. The user_1 login to the server
    3. the user_1 create channels
    4. Time to Test:
        1. test for more than 50 messages
        2. test for less than 50 messages
        3. test_start_is_10_and_not_50_messages
        4. test_start_is_10_and_50_messages
        5. input error: - Channel ID is not a valid channel
                        - start is greater than or equal to the total number of messages in the channel
        6. access error: - Authorised user is not a member of channel with channel_id
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




def test_10_messages_in_channel(register_and_login_user_1, create_public_channel):
    '''test for less than 50 messages '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    for _ in range(10):
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

    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'channel_id' : 1,
        'start': 0,
    })

    payload = load(urllib.request.urlopen(f"{BASE_URL}/channel/messages?{queryString}"))

    assert len(payload['messages']) == 10
    assert payload['end'] == -1

def test_50_messages_in_channel(register_and_login_user_1, create_public_channel):
    '''test for less than 50 messages '''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    for _ in range(50):
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

    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'channel_id' : 1,
        'start': 0,
    })

    payload = load(urllib.request.urlopen(f"{BASE_URL}/channel/messages?{queryString}"))

    assert len(payload['messages']) == 50
    assert payload['end'] == 50


def test_start_is_10_and_not_50_messages(register_and_login_user_1, create_public_channel):
    '''in this case, less than 50 messages left starts from 10'''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    for _ in range(50):
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

    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'channel_id' : 1,
        'start': 10,
    })

    payload = load(urllib.request.urlopen(f"{BASE_URL}/channel/messages?{queryString}"))

    assert len(payload['messages']) == 40
    assert payload['end'] == -1

def test_start_is_10_and_70_messages(register_and_login_user_1, create_public_channel):
    '''in this case, more than 50 messages left starts from 10'''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    for _ in range(70):
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

    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'channel_id' : 1,
        'start': 10,
    })

    payload = load(urllib.request.urlopen(f"{BASE_URL}/channel/messages?{queryString}"))

    assert len(payload['messages']) == 50
    assert payload['end'] == 60
def test_invalid_channel_id(register_and_login_user_1, create_public_channel):
    '''test for channel id is invalid'''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    for _ in range(10):
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

    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'channel_id' : 1231321,
        'start': 0,
    })

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{BASE_URL}/channel/messages?{queryString}")

def test_invalid_start(register_and_login_user_1, create_public_channel):
    '''start is greater than or equal to the total number of messages in the channel'''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    for _ in range(10):
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

    queryString = urllib.parse.urlencode({
        'token' : user_1_token,
        'channel_id' : 1231321,
        'start': 10,
    })

    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{BASE_URL}/channel/messages?{queryString}")

def test_unauthorised_user(register_and_login_user_1, create_public_channel):
    '''Authorised user is not a member of channel with channel_id'''
    user_1_token = 'b\'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1X2lkIjoiMSJ9.N0asY15U0QBAYTAzxGAvdkuWG6CyqzsR_rvNQtWBmLg\''
    for _ in range(10):
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

    invalid_token = 'this is not a valid token'
    queryString = urllib.parse.urlencode({
        'token' : invalid_token,
        'channel_id' : 1231321,
        'start': 10,
    })
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(f"{BASE_URL}/channel/messages?{queryString}")
