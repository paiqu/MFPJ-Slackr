from channel import channel_invite, channel_details, channel_messages 
from auth import auth_login, auth_register, auth_logout 
from channels import channels_create
import pytest
from error import InputError

def test_channel_invite_correct():
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['u_id']
    
    channel_invite('token', c_id1,u_id1)


#Tests if channel Exists
def test_channel_exist():
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['u_id']
    
    with pytest.raises(InputError) as e:
        channel_invite('token','c_id2', 'u_id1')
        

#Tests if valid user (if user exists)

def test_channel_valid_user():
    channel1 = channels_create('token', 'Channel1', True)
    c_id1=channe1['u_id']
    
    with pytest.raises(InputError) as e:
        channel_invite('token',c_id1, 'u_id2')

        
    
    
