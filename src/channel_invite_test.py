from channel import channel_invite, channel_details, channel_messages 
from auth import auth_login, auth_register, auth_logout 
from channels import channels_create
import pytest
from error import InputError, AccessError

"""
This test performs a test on the channel_invite function . This test is correct.
"""
def test_channel_invite_correct():
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['channel_id']
    
    channel_invite('token', c_id1,u_id1)

"""
This test checks to see if the channel has been created before inviting users
"""
def test_channel_exists_invite():
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['channel_id']
    
    with pytest.raises(InputError) as e:
        channel_invite('token','c_id2', 'u_id1')
        
"""
Tests to see if user is registered/existing when invited to channel
""" 
def test_channel_invite_invalid_user():
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['channel_id']
    
    with pytest.raises(InputError) as e:
        channel_invite('token',c_id1, 'u_id2')
        
        
#user added twice        
def test_channel_invite_user_twice():
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['channel_id']
    
    channel_invite('token', c_id1,u_id1)
    
    with pytest.raises(AccessError) as e:
        channel_invite('token', c_id1,u_id1)
       