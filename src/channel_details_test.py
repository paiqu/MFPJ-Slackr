from channel import channel_invite, channel_details, channel_messages 
from auth import auth_login, auth_register, auth_logout 
from channels import channels_create
import pytest
from error import InputError, AccessError


## THE FOLLOWING FUNCTIONS ARE TESTS FOR CHANNEL_DETAILS


def test_channel_details_correct():
    """
    This test performs a test on the channel_details function . This test is correct.
    """
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['channel_id']
    
    channel_invite('token', c_id1,u_id1)
    
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['u_id']
    
    assert channel_details('token', c_id1) == {
        'name' : 'Channel1',
        'owner_members': user1['u_id1's], 
        'all_members': user1['u_id1'],
    }    
        
    
        