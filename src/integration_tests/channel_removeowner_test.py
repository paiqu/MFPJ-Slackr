import pytest
from channel import channel_removeowner, channel_details, channel_join
from channels import channels_create
from error import InputError, AccessError
from auth import auth_register

'''
channel_removeowner(token, channel_id, u_id) -> {}

Remove user with user id u_id an owner of this channel

Input Error:
    1. invalid Channel ID
    2. user with user id is not an owner of the channel

AccessError:
    1. authorised user is not an owner of the slackr, 
       or an owner of this channel

Tests:
    1. success case
    2. inputError_1: invalid channel_id
    3. inputError_2: u_id is not owner
    4. accessError
'''

def test_channel_removeowner_success():
    # Register for user1
    user1 = auth_register('user1@unsw.edu.au', 'thisisaPassword', 'User', 'One')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # Register for user1
    user2 = auth_register('user2@unsw.edu.au', 'thisisaPasswordU2', 'User', 'Two')
    u_id2 = user2['u_id']
    token2 = user2['token']

    # user1 creates a public channel
    channel_id = (channels_create(token1, 'channel1', True))['channel_id']

    # user2 joins channel1
    channel_join(token2, channel_id)

    # owners before removing
    owners = (channel_details(token1, channel_id))['owner_members']

    # user1, as owner of slack, removes himself from channel1
    channel_removeowner(token1, channel_id, u_id1)

    # newOwners after removing
    newOwners = channel_details(token1, channel_id)['owner_members']

    assert len(newOwners) < len(owners)
    for x in newOwners:
        assert x["u_id"] != u_id1

def test_channel_removeowner_invalidChannelID():
    # Register for user1
    user1 = auth_register('user1@unsw.edu.au', 'thisisaPassword', 'User', 'One')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # user1 creates a public channel
    channel_id = (channels_create(token1, 'channel1', True))['channel_id']

    # invalid channel_id
    with pytest.raises(InputError):
        channel_removeowner(token1, channel_id + 5, u_id1)

def test_channel_removeowner_notOwner():
    # Register for user1
    user1 = auth_register('user1@unsw.edu.au', 'thisisaPassword', 'User', 'One')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # Register for user1
    user2 = auth_register('user2@unsw.edu.au', 'thisisaPasswordU2', 'User', 'Two')
    u_id2 = user2['u_id']
    token2 = user2['token']

    # user1 creates a public channel
    channel_id = (channels_create(token1, 'channel1', True))['channel_id']
    
    # u_id2 is not an owner of channel1
    with pytest.raises(InputError):
        channel_removeowner(token1, channel_id, u_id2)

def test_channel_removeowner_accessError():
    # Register for user1 (owner)
    user1 = auth_register('user1@unsw.edu.au', 'thisisaPassword', 'User', 'One')
    u_id1 = user1['u_id']
    token1 = user1['token']

    # Register for user1
    user2 = auth_register('user2@unsw.edu.au', 'thisisaPasswordU2', 'User', 'Two')
    u_id2 = user2['u_id']
    token2 = user2['token']
  
    # user1 creates a public channel
    channel_id = (channels_create(token1, 'channel1', True))['channel_id']

    with pytest.raises(AccessError):
        channel_removeowner(token2, channel_id, u_id1)
