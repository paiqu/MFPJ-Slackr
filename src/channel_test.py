from channel import channel_invite, channel_details, channel_messages 
from auth import auth_login, auth_register, auth_logout 
from channels import channels_create
import pytest
from error import InputError, AccessError

def test_channel_invite_correct():
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['channel_id']
    
    channel_invite('token', c_id1,u_id1)


#Tests if channel Exists
def test_channel_exists_invite():
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['channel_id']
    
    with pytest.raises(InputError) as e:
        channel_invite('token','c_id2', 'u_id1')
        

#Tests if valid user (if user exists)

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
        
## THE FOLLOWING FUNCTIONS ARE TESTS FOR CHANNEL_DETAILS

def test_channel_details_correct():
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
        'owner_members': [u_id1], 
        'all_members': [u_id1],
    }    
        
    
        
    
    
