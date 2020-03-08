import pytest
from auth import auth_register
from error import InputError, AccessError
from message import message_send, message_remove
from channels import channels_create
from channel import channel_join, channel_messages

'''
This is a test file for message_remove function

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
    
    '''
    a normal case test (the sender remove the message he sent in a private channel)
    '''
    # register for a new user
    newUser = auth_register('z47123898@unsw.edu.au', 'safjiefijew322', 'Lei', 'Zhang')
    newUser_id = newUser['u_id']
    newUser_token = newUser['token']
    
    # create a channel
    newChannel = channels_create(newUser_token, 'General', False)
    channel_ID = newChannel['channel_id']

    # send message 
    sending = message_send(newUser_token, channel_ID, 'Nice to meet u')
    message_id = sending['message_id']

    # remove message (the sender)
    message_remove(newUser_token, message_id)

    # list channel messages
    messageReturn = channel_messages(newUser_token, channel_ID, 0)
    
    # checking
    assert len(messageReturn['messages']) == 0
    
def test_message_remove_case2():

    '''
    a normal case test (the admin remove the message in a public channel)
    '''
       
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

    # list channel messages
    messageReturn1 = channel_messages(newUser1_token, channel_ID1, 0)
    
    # checking
    assert len(messageReturn1['messages']) == 0

def test_message_remove_inputError():

    '''
    test for the inputError case when message ID no longer exists.
    '''
    
    # register for a new user
    newUser3 = auth_register('z47123898@unsw.edu.au', 'safjiefijew322', 'Lei', 'Zhang')
    newUser3_id = newUser3['u_id']
    newUser3_token = newUser3['token']
    
    # create a channel
    newChannel2 = channels_create(newUser3_token, 'General', True)
    channel_ID2 = newChannel2['channel_id']

    # send message 
    sending2 = message_send(newUser3_token, channel_ID2, 'Nice to meet u')
    message_id2 = sending2['message_id']

    # remove message with non-existent message_id (Inputerror)
    with pytest.raises(InputError):
        message_remove(newUser3_token, message_id2 + 5)

def test_message_remove_accessError():

    '''
    test for the accessError case when authorised user is not the admin as well
    as the sender.
    '''
    
    # register for new users
    newUser4 = auth_register('z5237609@unsw.edu.au', 'Zxl471238986', 'Matty', 'Zhang')
    newUser4_id = newUser4['u_id']
    newUser4_token = newUser4['token']

    newUser5 = auth_register('z1234567@unsw.edu.au', 'dfhsiH4723', 'First', 'Last')
    newUser5_id = newUser5['u_id']
    newUser5_token = newUser5['token']

    newUser6 = auth_register('z5453673@unsw.edu.au', 'dfh4f324r23', 'Fan', 'LI')
    newUser6_id = newUser6['u_id']
    newUser6_token = newUser6['token']
            
    # user4 create a channel
    newChannel3 = channels_create(newUser4_token, 'General', True)
    channel_ID3 = newChannel3['channel_id']

    # user5 6 join this channel
    channel_join(newUser5_token, channel_ID3)
    channel_join(newUser6_token, channel_ID3)
    
    # user6 send a message 
    sending3 = message_send(newUser6_token, channel_ID3, 'Nice to meet u')
    message_id3 = sending3['message_id'] 
    
    # user5 remove message (user5 is not the admin and the sender) (Accesserror)
    with pytest.raises(AccessError):  
        message_remove(newUser5_token, message_id3)

