import pytest
from auth import auth_register
from channels import channels_create
from message import message_send
from other import search

'''
search(token, query_str) -> {messages}

Given a query string, return a collection of messages in 
all of the channels that the user has joined that match the query

No exception

ASSUME: messgaes in private channel can be searched
        capital-sensitive

Tests:
    1. user1 joins one channel
    2. user1 joins several channels
'''

def test_search_1():
    # when there is only one channel
    # register a user1
    user1 = auth_register("user1@unsw.edu.au", "superStrongPassword123", "User", "One")
    u_id1 = user1['u_id']
    token1 = user1['token']

    # user1 creates a channel
    channel_1 = channels_create(token1, "channel1", True)
    channel_id = channel_1['channel_id']

    # user1 sends some msgs
    msg1 = message_send(token1, channel_id, "hello")
    msg_id_1 = msg1['message_id']

    msg2 = message_send(token1, channel_id, "Bye")
    msg_id_2 = msg2['message_id']

    msg3 = message_send(token1, channel_id, "hello")
    msg_id_3 = msg3['message_id']



    query = 'hello'
    messages = search(token1, query)
    
    #msgList is a list of dicts
    msgList = messages['messages']

    assert len(msgList) == 2

    for x in msgList:
        assert x['message'] == 'hello'



def test_search_2():
    #search msgs from two different channels
    # register a user1
    user1 = auth_register("user1@unsw.edu.au", "superStrongPassword123", "User", "One")
    u_id1 = user1['u_id']
    token1 = user1['token']

    # user1 creates a channel
    channel_1 = channels_create(token1, "channel1", True)
    channel_id = channel_1['channel_id']

    # user1 sends some msgs
    msg1 = message_send(token1, channel_id, "hello")
    msg_id_1 = msg1['message_id']

    msg2 = message_send(token1, channel_id, "Bye")
    msg_id_2 = msg2['message_id']

    msg3 = message_send(token1, channel_id, "hello")
    msg_id_3 = msg3['message_id']



    # user1 creates a new channel
    channel_2 = channels_create(token1, "channel1", True)
    channel_id_2 = channel_2['channel_id']

    # user1 sends some msgs
    msg4 = message_send(token1, channel_id_2, "hello")
    msg_id_4 = msg4['message_id']

    msg5 = message_send(token1, channel_id_2, "Bye")
    msg_id_5 = msg5['message_id']

    msg6 = message_send(token1, channel_id_2, "hello")
    msg_id_6 = msg6['message_id']

    query = 'hello'
    messages = search(token1, query)
    
    #msgList is a list of dicts
    msgList = messages['messages']

    assert len(msgList) == 4

    for x in msgList:
        assert x['message'] == 'hello'

def test_search_3():
    # test case sensitive
    # register a user1
    user1 = auth_register("user1@unsw.edu.au", "superStrongPassword123", "User", "One")
    u_id1 = user1['u_id']
    token1 = user1['token']

    # user1 creates a channel
    channel_1 = channels_create(token1, "channel1", True)
    channel_id = channel_1['channel_id']

    # user1 sends some msgs
    msg1 = message_send(token1, channel_id, "hello")
    msg_id_1 = msg1['message_id']

    msg2 = message_send(token1, channel_id, "Bye")
    msg_id_2 = msg2['message_id']

    msg3 = message_send(token1, channel_id, "HELLO")
    msg_id_3 = msg3['message_id']



    query = 'HELLO'
    messages = search(token1, query)
    
    #msgList is a list of dicts
    msgList = messages['messages']

    assert len(msgList) == 1

    for x in msgList:
        assert x['message'] == 'HELLO'
