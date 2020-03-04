import pytest
from auth import auth_register
from error import InputError, AccessError
from message import message_send, message_remove
from channels import channels_create
from channel import channel_join

'''
This is a test file for message_remove function

InputError: Message (based on ID) no longer exists
AccessError: 

1. test for normal case 
    (Given a message_id for a message, 
    this message is removed from the channel)
    
2. test for InputError
    Message (based on ID) no longer exists
    
3. test for AccessError

    when none of the following are true:
    
    1.Message with message_id was sent by 
    the authorised user making this request
    
    2.The authorised user is an admin or owner 
    of this channel or the slackr
    
'''

def test_message_remove_case1():

    # register for a new user
    newUser = auth_register('z47123898@unsw.edu.au', 'safjiefijew322', 'Lei', 'Zhang')
    newUser_id = newUser['u_id']
    newUser_token = newUser['token']
    
    # create a channel
    newChannel = channels_create(newUser_token, 'General', True)
    channel_ID = newChannel['channel_id']

    # send message 
    sending = message_send(newUser_token, channel_ID, 'Nice to meet u')
    message_id = sending['message_id']

    # remove message
    message_remove(newUser_token, message_id)
    assert message_id == None
    
def test_message_remove_case2():
    
    # register for a new user
    newUser1 = auth_register('z5237609@unsw.edu.au', 'Zxl471238986', 'Matty', 'Zhang')
    newUser1_id = newUser1['u_id']
    newUser1_token = newUser1['token']

    newUser2 = auth_register('z1234567@unsw.edu.au', 'dfhsiH4723', 'First', 'Last')
    newUser2_id = newUser2['u_id']
    newUser2_token = newUser2['token']
        
    # create a channel
    newChannel1 = channels_create(newUser1_token, 'General', True)
    channel_ID1 = newChannel1['channel_id']

    # user2 join this channel
    channel_join(newUser2_token, channel_ID1)
    
    # user2 send a message 
    sending1 = message_send(newUser2_token, channel_ID1, 'Nice to meet u')
    message_id1 = sending1['message_id'] 
    
    # user1 (admin) remove it    
    message_remove(newUser1_token, message_id1)
    assert message_id1 == None 

