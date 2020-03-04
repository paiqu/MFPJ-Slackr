import pytest
from auth import auth_register
from error import InputError
from channels import channels_create, channels_list
from channel import channel_join

'''
This is a test file for channels_create function

InputError: name is more than 20 characters long

1. test for normal case 
    (Creates a new channel with that name 
    that is either a public or private channel)
    
2. test for InputError
    when name is more than 20 characters long
'''

def test_user_profile():
    
    # register for new users
    newUser1 = auth_register('z5237609@unsw.edu.au', 'Zxl471238986', 'Matty', 'Zhang')
    newUser1_id = newUser1['u_id']
    newUser1_token = newUser1['token']

    newUser2 = auth_register('z1234567@unsw.edu.au', 'Zfheiu3H33', 'Foster', 'Chen')
    newUser2_id = newUser2['u_id']
    newUser2_token = newUser2['token']    
    
    # create a channel
    newChannel = channels_create(newUser1_token, 'General', True)
    channel_ID = newChannel['channel_id']
    
    # add user into new channel
    channel_join(newUser2_token, channel_ID)
    
    # make sure User1 and User2 both in new channel
    channel_list1 = channels_list(newUser1_token)
    channel_list2 = channels_list(newUser2_token)

    assert channel_list1 == channel_list2

def test_user_profile_inputError():
    
    # register for a new user
    newUser3 = auth_register('z7654321@unsw.edu.au', 'dhf4830ZH6', 'First', 'Last')
    newUser3_id = newUser3['u_id']
    newUser3_token = newUser3['token']
    
    # create a channel (inputerror)
    with pytest.raises(InputError):
        channels_create(newUser3_token, 'GeneralGeneralGeneral', True)
