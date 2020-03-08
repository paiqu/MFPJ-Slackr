from channel import channel_leave, channel_join
from channels import channels_create, channels_list
import pytest
from error import InputError, AccessError
from auth import auth_register

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
        * user is a member
        * user is a owner
    2. test for Input Error: invalid channel_id
    3. test for Access Error: notmember
'''


def test_channel_leave_memberLeave():
    # Register for user1
    user1 = auth_register('user1@unsw.edu.au', 'thisisaPassword', 'User', 'One')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # Register for user2
    user2 = auth_register('user2@unsw.edu.au', 'thisisaPassword', 'User', 'Two')
    u_id2 = user2['u_id']
    token2 = user2['token']

    # user1 creates a public channel named "channel1"
    channel_id = (channels_create(token1, 'channel1', True))['channel_id']

    # user2 joins channel1
    channel_join(token2, channel_id)

    # channelList is a list of channel in which user2 is before the removal
    channelList = (channels_list(token2))["channels"]

    # remove user2 from channel1
    channel_leave(token2, channel_id)

    # newChannelList is the list of channel in which user2 is after the removal
    newChannelList = (channels_list(token2))["channels"]

    assert len(channelList) != len(newChannelList)
    assert newChannelList == []



def test_channel_leave_ownerLeave():
    # Register for user1
    user1 = auth_register('user1@unsw.edu.au', 'thisisaPassword', 'User', 'One')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # Register for user2
    user2 = auth_register('user2@unsw.edu.au', 'thisisaPassword', 'User', 'Two')
    u_id2 = user2['u_id']
    token2 = user2['token']

    # user1 creates a public channel named "channel1"
    channel_id = (channels_create(token1, 'channel1', True))['channel_id']

    # user2 joins channel1
    channel_join(token2, channel_id)

    # channelList is a list of channel in which user1 is before the removal
    channelList = (channels_list(token1))["channels"]

    # remove user1 from channel1
    channel_leave(token1, channel_id)

    # newChannelList is the list of channel in which user2 is after the removal
    newChannelList = (channels_list(token1))["channels"]

    assert len(channelList) != len(newChannelList)
    assert newChannelList == []

def test_channel_leave_success():
    # Register for user1
    user1 = auth_register('user1@unsw.edu.au', 'thisisaPassword', 'User', 'One')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # Register for user2
    user2 = auth_register('user2@unsw.edu.au', 'thisisaPassword', 'User', 'Two')
    u_id2 = user2['u_id']
    token2 = user2['token']

    # user1 creates a public channel named "channel1"
    channel_id1 = (channels_create(token1, 'channel1', True))['channel_id']
    channel_id2 = (channels_create(token1, 'channel2', True))['channel_id']
    channel_id3 = (channels_create(token1, 'channel3', True))['channel_id']

    # user2 joins channel1
    channel_join(token2, channel_id1)
    channel_join(token2, channel_id2)
    channel_join(token2, channel_id3)

    # channelList is a list of channel in which user2 is before the removal
    channelList = (channels_list(token2))["channels"]

    # remove user2 from channel1
    channel_leave(token2, channel_id2)

    # newChannelList is the list of channel in which user2 is after the removal
    newChannelList = (channels_list(token2))["channels"]

    assert len(channelList) != len(newChannelList)
    for x in newChannelList:
        assert x["channel_id"] != channel_id2

def test_channel_leave_invalidChannelID():
    # Register for user1
    user1 = auth_register('user1@unsw.edu.au', 'thisisaPassword', 'User', 'One')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # Register for user2
    user2 = auth_register('user2@unsw.edu.au', 'thisisaPassword', 'User', 'Two')
    u_id2 = user2['u_id']
    token2 = user2['token']

    # user1 creates a public channel named "channel1"
    channel_id = (channels_create(token1, 'channel1', True))['channel_id']

    # user2 joins channel1
    channel_join(token2, channel_id)
    
    with pytest.raises(InputError):
        channel_leave(token2, channel_id+5)

def test_channel_leave_notMember():
    # when Authorised user is not a member of channel with channel_id'
    user1 = auth_register('z123456@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    u_id1 = user1['u_id']
    token1 = user1['token']

    user2 = auth_register('z654321@unsw.edu.au', 'thisisaGoodPassword', 'New', 'Guy')
    u_id2 = user2['u_id']
    token2 = user2['token']

    # user1 create a channel
    channel_id = (channels_create(token1, 'channel1', True))['channel_id']
    
    with pytest.raises(AccessError):
        channel_leave(token2, channel_id)

    















