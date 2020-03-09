import pytest

from channel import channel_invite, channel_details, channel_messages 
from auth import auth_login, auth_register, auth_logout 
from channels import channels_create
from error import InputError, AccessError

def test_channel_invite_correct():
    """
    This test performs a test on the channel_invite function . This test is correct.
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
    channel1_details = channel_details(user1_token, c_id1)

    
    #As the channel invite function doesn't return anything, 
    # we can use the channel_details function to test this. 
    #The invited user is the second member of the channel 
    assert u_id2 == channel1_details[['all_members'][1]['u_id']]
    
def test_channel_exists_invite():
    """
    Returns error when channel_id does not refer to a valid channel.
    This test checks to see if the channel has been created before inviting users.
    """ 
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1 = user1['u_id']
    user1_token = user1['token']

    user2 = auth_register('MFPJ@unsw.edu.au','!987bye', 'Student', 'Test')
    u_id2 = user2['u_id']
    user2_token = user2['token']
    
    channel1 = channels_create(user1_token , 'Channel_MFPJ', True)
    c_id1 = channel1['channel_id']
    
    
    with pytest.raises(InputError):
        channel_invite(user1_token, c_id1 + 5, u_id2)
        

def test_channel_invite_invalid_user():

    '''
    Tests to see if user is registered/existing when invited to channel
    '''
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1 = user1['u_id']
    user1_token = user1['token']

    user2 = auth_register('MFPJ@unsw.edu.au','!987bye', 'Student', 'Test')
    u_id2 = user2['u_id']
    user2_token = user2['token']

    channel1 = channels_create(user1_token, 'Channel1', True)
    c_id1 = channel1['channel_id']
    
    with pytest.raises(InputError):
        channel_invite(user1_token, c_id1, u_id2 + 5)
        
        

def test_channel_invite_user_twice():

    """
    When a user is added to the channel twice.
    """
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1 = user1['u_id']
    user1_token = user1['token']

    user2 = auth_register('MFPJ@unsw.edu.au','!987bye', 'Student', 'Test')
    
    u_id2 = user2['u_id']
    user2_token = user2['token']
    
    channel1 = channels_create(user1_token, 'Channel1', True)
    c_id1=channel1['channel_id']
    
    channel_invite(user1_token, c_id1,u_id2)
    
    with pytest.raises(InputError):
        channel_invite(user1_token, c_id1,u_id2)

def test_nonmember_adds_user():
    '''
    A user who is not part of a channel himself, is not allowed to invite another user to that channel.
    I.e. A user must be a member of the channel themselves before inviting someone else.
    '''   
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test') 

    u_id1 = user1['u_id']
    user1_token = user1['token']

    user2 = auth_register('MFPJ@unsw.edu.au','!987bye', 'Student', 'Test')
    u_id2 = user2['u_id']
    user2_token = user2['token']
    
    user3 = auth_register('git@unsw.edu.au','!987password', 'Jane', 'Smith')
    u_id3 = user3['u_id']
    user3_token = user3['token']
    
    channel1 = channels_create(user1_token, 'Channel1', True)
    c_id1 = channel1['channel_id']
    
    with pytest.raises(AccessError):
        channel_invite(user2_token, c_id1,u_id3)
