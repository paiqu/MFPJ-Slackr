import pytest
from auth import auth_register
from error import InputError, AccessError
from message import message_send
from channels import channels_create

'''
This is a test file for message_send function

InputError: Message is more than 1000 characters
AccessError: The authorised user has not joined the channel 
             they are trying to post to

1. test for normal case 
    (Send a message from authorised_user to 
    the channel specified by channel_id)
    
2. test for InputError
    Message is more than 1000 characters
    
3. test for AccessError
    The authorised user has not joined the channel 
    they are trying to post to
'''

def test_message_send_inputError():
    
    # register for a new user
    newUser1 = auth_register('z5237609@unsw.edu.au', 'Zxl471238986', 'Matty', 'Zhang')
    newUser1_id = newUser1['u_id']
    newUser1_token = newUser1['token']
    
    # create a channel
    newChannel = channels_create(newUser1_token, 'General', True)
    channel_ID = newChannel['channel_id']

    # send message (inputerror)
    with pytest.raises(InputError):
        message_send(newUser1_token, channel_ID, 'a' * 1001)

def test_message_send_accessError():
    
    # register for new users
    newUser2 = auth_register('z1234567@unsw.edu.au', 'dfhsiH4723', 'First', 'Last')
    newUser2_id = newUser2['u_id']
    newUser2_token = newUser2['token']

    newUser3 = auth_register('z7654321@unsw.edu.au', '4298dhihiHIh', 'Foster', 'Chen')
    newUser3_id = newUser3['u_id']
    newUser3_token = newUser3['token']
        
    # create a channel
    newChannel_1 = channels_create(newUser2_token, 'Random', True)
    channel_ID_1 = newChannel_1['channel_id']

    # send message (inputerror)
    with pytest.raises(AccessError):
        message_send(newUser3_token, channel_ID_1, 'Hello World')    


