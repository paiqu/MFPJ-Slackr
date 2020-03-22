import pytest
from channels import channels_create, channels_list
from error import InputError, AccessError
from auth import auth_register
from channel import channel_join
'''
channel_join(token, channel_id) -> {}


Input Error:
    Channel ID is not a valid channel

Access Error:
    Channel_id refers to a channel that is private (when the authorised user is not an admin)

Tests:
    1. successful case: B join A's public channel
    2. invalid channel_id
    3. B join A's private channel

'''

def test_channel_join_success_1():
    # test user2 joins user1's channel

    # Register for user1
    user1 = auth_register('user1@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    u_id1 = user1['u_id']
    token1 = user1['token']

    channel_id = (channels_create(token1, 'channel1', True))['channel_id']

    # Register for user2
    user2 = auth_register('user2@unsw.edu.au', 'thisisaGoodPassword', 'New', 'Guy')
    u_id2 = user2['u_id']
    token2 = user2['token']

    # user2 join user1's channel now
    channel_join(token2, channel_id)

    list2 = channels_list(token2)["channels"]

    assert len(list2) == 1
    assert list2[0]["channel_id"] == channel_id
    assert list2[0]["name"] == "channel1"

def test_channel_join_success_2():
    # test user2 joins 3 channels

    # Register for user1
    user1 = auth_register('user1@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    u_id1 = user1['u_id']
    token1 = user1['token']

    channel_id1 = (channels_create(token1, 'channel1', True))['channel_id']
    channel_id2 = (channels_create(token1, 'channel2', True))['channel_id']
    channel_id3 = (channels_create(token1, 'channel3', True))['channel_id']

    # Register for user2
    user2 = auth_register('user2@unsw.edu.au', 'thisisaGoodPassword', 'New', 'Guy')
    u_id2 = user2['u_id']
    token2 = user2['token']

    # user2 join user1's channels now
    channel_join(token2, channel_id1)
    channel_join(token2, channel_id2)
    channel_join(token2, channel_id3)

    list1 = channels_list(token1)["channels"]
    list2 = channels_list(token2)["channels"]

    assert len(list1) == len(list2)
    assert len(list2) == 3



def test_channel_inputError():
    # Register for user1
    user1 = auth_register('z123456@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # Register for user2
    user2 = auth_register('user2@unsw.edu.au', 'thisisaGoodPassword', 'New', 'Guy')
    u_id2 = user2['u_id']
    token2 = user2['token']

    channel_id1 = (channels_create(token1, 'channel1', True))['channel_id']

    # invalid channel_id
    with pytest.raises(InputError):
        channel_join(token2, channel_id1 + 5)

def test_channel_accessError():
    # Register for user1
    user1 = auth_register('z123456@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # user1 creates a PRIVATE channel
    channel_id = (channels_create(token1, 'channel1', False))['channel_id']

    # Register for user2
    user2 = auth_register('z654321@unsw.edu.au', 'thisisaGoodPassword', 'New', 'Guy')
    u_id2 = user2['u_id']
    token2 = user2['token']

    # user2 joins user1's private channel
    with pytest.raises (AccessError):
        channel_join(token2, channel_id)

        
