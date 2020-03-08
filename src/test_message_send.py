import pytest
from auth import auth_register
from error import InputError, AccessError
from message import message_send
from channel import channel_invite, channel_messages, channel_join, channel_leave
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

def test_message_send_case1():

    '''
    a normal case test (send message in a public channel)
    '''
    
    # register for a new user
    newUser = auth_register('z47123898@unsw.edu.au', 'safjiefijew322', 'Lei', 'Zhang')
    newUser_id = newUser['u_id']
    newUser_token = newUser['token']
    
    # create a channel
    newChannel_2 = channels_create(newUser_token, 'General', True)
    channel_ID_2 = newChannel_2['channel_id']

    # send message
    sending = message_send(newUser_token, channel_ID_2, 'Nice to meet u')
    message_id = sending['message_id']

    # list channel messages
    messageReturn = channel_messages(newUser_token, channel_ID_2, 0)
    
    # checking
    assert messageReturn['messages'][0]['message_id'] == message_id



def test_message_send_case2():

    '''
    a normal case test (send message in a private channel)
    (more users, more messages)
    '''
    
    # register for new users
    newUser4 = auth_register('z47123898@unsw.edu.au', 'safjiefijew322', 'Lei', 'Zhang')
    newUser4_id = newUser4['u_id']
    newUser4_token = newUser4['token']

    newUser5 = auth_register('z5237609@unsw.edu.au', 'Zxl471238986', 'Matty', 'Zhang')
    newUser5_id = newUser5['u_id']
    newUser5_token = newUser5['token']
        
    # create a channel
    newChannel_3 = channels_create(newUser4_token, 'General', False)
    channel_ID_3 = newChannel_3['channel_id']
    
    # invite user
    channel_invite(newUser4_token, channel_ID_3, newUser5_id)

    # send message
    sending1 = message_send(newUser4_token, channel_ID_3, 'Nice to meet u.')
    message_id1 = sending1['message_id']

    sending2 = message_send(newUser5_token, channel_ID_3, 'Nice to meet u too.')
    message_id2 = sending2['message_id']
    
    sending3 = message_send(newUser4_token, channel_ID_3, 'How are you?')
    message_id3 = sending3['message_id']

    sending4 = message_send(newUser5_token, channel_ID_3, 'I am good.')
    message_id4 = sending4['message_id']
        
    # list channel messages
    messageReturn1 = channel_messages(newUser4_token, channel_ID_3, 0)
    
    # checking
    assert messageReturn1['messages'][0]['message_id'] == message_id4
    assert messageReturn1['messages'][1]['message_id'] == message_id3  
    assert messageReturn1['messages'][2]['message_id'] == message_id2
    assert messageReturn1['messages'][3]['message_id'] == message_id1


            
def test_message_send_inputError():

    '''
    test for the inputError case when message is more than 1000 characters.
    '''
    
    # register for a new user
    newUser1 = auth_register('z5237609@unsw.edu.au', 'Zxl471238986', 'Matty', 'Zhang')
    newUser1_id = newUser1['u_id']
    newUser1_token = newUser1['token']
    
    # create a channel
    newChannel = channels_create(newUser1_token, 'General', True)
    channel_ID = newChannel['channel_id']

    # send message with more than 1000 characters (inputerror)
    with pytest.raises(InputError):
        message_send(newUser1_token, channel_ID, 'a' * 1001)


def test_message_send_accessError_case1():

    '''
    test for the accessError case when the authorised user has not joined the 
    channel
    '''
    
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

    # send message with an unauthorised user (accesserror)
    with pytest.raises(AccessError):
        message_send(newUser3_token, channel_ID_1, 'Hello World')    



def test_message_send_accessError_case2():

    '''
    test for the accessError case when the authorised user has joined the 
    channel but removed
    '''
    
    # register for new users
    newUser6 = auth_register('z1234567@unsw.edu.au', 'dfhsiH4723', 'First', 'Last')
    newUser6_id = newUser6['u_id']
    newUser6_token = newUser6['token']

    newUser7 = auth_register('z7654321@unsw.edu.au', '4298dhihiHIh', 'Foster', 'Chen')
    newUser7_id = newUser7['u_id']
    newUser7_token = newUser7['token']
        
    # create a channel
    newChannel_4 = channels_create(newUser6_token, 'Random', True)
    channel_ID_4 = newChannel_4['channel_id']
    
    # join channel
    channel_join(newUser7_token, channel_ID_4)
    
    # leave this channel
    channel_leave(newUser7_token, channel_ID_4)
    
    # send message with an unauthorised user (accesserror)
    with pytest.raises(AccessError):
        message_send(newUser7_token, channel_ID_4, 'Hello World')  
