import pytest

from channel import channel_invite, channel_details, channel_messages 
from auth import auth_login, auth_register, auth_logout 
from channels import channels_create

from error import InputError, AccessError

def test_channel_details_correct():
    """
    This test performs a test on the channel_details function . This test is correct.
    """
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1 = user1['u_id']
    user1_token = user1['token']

    user2= auth_register('MFPJ@unsw.edu.au','!987bye', 'Student', 'Test')
    u_id2 = user2['u_id']
    user2_token = user2['token']

    channel1 = channels_create(user1_token, 'Channel_MFPJ', True)
    c_id1 = channel1['channel_id']
    
    
    channel_invite(user1_token, c_id1,u_id2)

    channel1_details = channel_details(user1_token, c_id1)
    
    ## compare user ID of a user who we know is the owner member 
    assert u_id1 == channel1_details['owner_members'][0]['u_id']

def test_invalid_channelID():
    """
    Channel ID is not a valid channel
    """
    
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1 = user1['u_id']
    user1_token = user1['token']

    user2 = auth_register('MFPJ@unsw.edu.au','!987bye', 'Student', 'Test')
    u_id2 = user2['u_id']
    user2_token = user2['token']

    channel1 = channels_create(user1_token, 'Channel_MFPJ', True)
    c_id1 = channel1['channel_id']
    
    channel_invite(user1_token, c_id1,u_id2)

    with pytest.raises(AccessError):
        channel_details(user1_token, c_id1 + 5)

    
def test_nonmember_asks_details():
    '''
    A user who is not part of a channel himself, is not allowed to ask details about that channel 
    I.e. A user must be a member of the channel themselves before requesting channel details 
    '''   
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1 = user1['u_id']
    user1_token = user1['token']

    user2 = auth_register('MFPJ@unsw.edu.au','!987bye', 'Student', 'Test')
    u_id2 = user2['u_id']
    user2_token = user2['token']
    
    user3 = auth_register('git@unsw.edu.au','!987password', 'Jane', 'Smith')
    u_id3=user3['u_id']
    user3_token = user3['token']
    
    channel1 = channels_create(user1_token, 'Channel1', True)
    c_id1 = channel1['channel_id']
    
    
    with pytest.raises(InputError):
        channel_details(user3_token, c_id1)
