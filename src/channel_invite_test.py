from channel import channel_invite, channel_details, channel_messages 
from auth import auth_login, auth_register, auth_logout 
from channels import channels_create
import pytest
from error import InputError, AccessError


def test_channel_invite_correct():
    """
    This test performs a test on the channel_invite function . This test is correct.
    """
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['channel_id']
    
    channel_invite('token', c_id1,u_id1)


def test_channel_exists_invite():
    """
    This test checks to see if the channel has been created before inviting users
    """ 
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['channel_id']
    
    with pytest.raises(InputError) as e:
        channel_invite('token','c_id2', 'u_id1')
        

def test_channel_invite_invalid_user():
    """
    Tests to see if user is registered/existing when invited to channel
    """ 
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['channel_id']
    
    with pytest.raises(InputError) as e:
        channel_invite('token',c_id1, 'u_id2')
        
        
#user added twice        
def test_channel_invite_user_twice():
    """
    When a user is added to the channel twice.
    """
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['channel_id']
    
    channel_invite('token', c_id1,u_id1)
    
    with pytest.raises(AccessError) as e:
        channel_invite('token', c_id1,u_id1)
       