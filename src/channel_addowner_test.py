import pytest
from channel import channel_addowner, channel_details
from channels import channels_create
from error import InputError, AccessError
from auth import auth_register

'''
channel_addowner(token, channel_id, u_id) -> {}

Make user with user id u_id an owner of this channel

InputError:
    1. Channel ID is not a valid channel
    2. When user with user id u_id is already an owner of the channel

AccessError:
    1. When the authorised user is not an owner of the slack or an owner of the channel

Tests:
    1. succuess: user2 become the owner of user1's channel
    2. InputError_1: invalid channel_id
    3. InputError_2: add A as its own channel's owner
    4. AccessError

ASSUME: there could be multiple owners for one channel
'''

def test_channel_addowner_success():
    # Register for user1
    user1 = auth_register('z123456@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # Register for user2
    user2 = auth_register('z654321@unsw.edu.au', 'thisisaGoodPassword', 'New', 'Guy')
    u_id2 = user2['u_id']
    token2 = user2['token']


    # user1 creates a public channel
    channel_id = (channels_create(token1, 'channel1', True))['channel_id']

    owners = (channel_details(token1, u_id1))['owner_members']

    # add user2 as an owner
    channel_addowner(token1, channel_id, u_id2)

    # owner is a list of dictionaries, 
    # where each dictionary contains types { u_id, name_first, name_last } 
    new_owners = (channel_details(token1, u_id1))['owner_members']

    assert len(owners) < len(new_owners)
    assert len(new_owners) == 2

def test_channel_addowner_inputError_1():
    # Register for user1
    # now user1 is the owner of the slackr
    user1 = auth_register('z123456@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # invalid channel_id
    with pytest.raises(InputError):
        channel_addowner(token1, 6, u_id1)

def test_channel_addowner_inputError_2():
    # Register for user1
    user1 = auth_register('z123456@unsw.edu.au', 'thisisaPassword', 'First', 'Last')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # user1 creates a public channel
    channel_id = (channels_create(token1, 'channel1', True))['channel_id']

    # user1 is already an owner of the channel
    with pytest.raises(InputError):
        channel_addowner(token1, channel_id, u_id1)

def test_channel_addowner_accessError_1():
    # Register for user1
    user1 = auth_register('user1@unsw.edu.au', 'user1Password123123', 'User', 'One')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # Register for user2
    user2 = auth_register('user2@unsw.edu.au', 'user2Password123123', 'User', 'Two')
    u_id2 = user2['u_id']
    token2 = user2['token']

    channel_id = channels_create(token1, 'newChannel', True)

    # authorised user is not owner of slackr or channel
    with pytest.raises(AccessError):
        channel_addowner(token2, channel_id, u_id2)