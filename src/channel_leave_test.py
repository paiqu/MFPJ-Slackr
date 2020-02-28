from channel import leave
from channels import create, list
import pytest
from error import InputError, AccessError
from auth import register

# def leave(token, channel_id)
# Given a channel ID, the user removed as a member of this channel
'''
    Input Error when
        Channel ID is not a valid channel

    Access Error when
        Authorised user is not a member of channel with channel_id'

    channels_create(token, name, is_public) -> {channel_id}
    auth_register(email, password, name_first, name_last) -> {u_id, token}

    1. test for successful leave
    2. test for Input Error
    3. test for Access Error
'''


def test_channel_leave_success():
    # Register for a user
    reg = register('z123456@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    u_id = reg['u_id']
    token = reg['token']

    # create a public channel named "Channel1"
    channel_id = (create(token, 'channel1', True))['channel_id']
    channel_list = list(token)

    leave(token, channel_id)

    channel_newList = list(token)

    assert channel_list != channel_newList

def test_channel_leave_inputError():
    # when channle ID is not a valid channel
    reg = register('z123456@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    token = reg['token']

    # create a public channel named "Channel1"
    channel_id = (create(token, 'channel1', True))['channel_id']
    
    with pytest.raises(InputError):
        leave(token, channel_id+5)

def test_channel_leave_accessError():
    # when Authorised user is not a member of channel with channel_id'
    user1 = register('z123456@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    u_id1 = user1['u_id']
    token1 = user1['token']

    user2 = register('z654321@unsw.edu.au', 'thisisaGoodPassword', 'New', 'Guy')
    u_id2 = user2['u_id']
    token2 = user2['token']

    # user1 create a channel
    channel_id = (create(token1, 'channel1', True))['channel_id']
    with pytest.raises(AccessError):
        leave(token2, channel_id)

    















