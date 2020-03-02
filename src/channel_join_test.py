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

def test_channel_join_success():

    # Register for user1
    user1 = auth_register('z123456@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    u_id1 = user1['u_id']
    token1 = user1['token']

    channel_id = (channels_create(token1, 'channel1', True))['channel_id']

    # Register for user2
    user2 = auth_register('z654321@unsw.edu.au', 'thisisaGoodPassword', 'New', 'Guy')
    u_id2 = user2['u_id']
    token2 = user2['token']

    # user2 join user1's channel now

    channel_join(token2, channel_id)

    list1 = channels_list(token1)
    list2 = channels_list(token2)

    assert list1 == list2

def test_channel_inputError():
    # Register for user1
    user1 = auth_register('z123456@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    u_id1 = user1['u_id']
    token1 = user1['token']

    with pytest.raises(InputError):
        channel_join(token1, 123456)

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

    with pytest.raises (AccessError):
        channel_join(token2, channel_id)

        
