import pytest
from auth import auth_register
from error import InputError
from channels import channels_create, channels_listall
from channel import channel_join

'''
This is a test file for channels_create function

InputError: name is more than 20 characters long

1. test for 2 normal cases 
    (Creates a new channel with that name 
    that is either a public or private channel)
    
2. test for InputError
    when name is more than 20 characters long
'''

def test_channels_create_case1():
    
    '''
    create a public channel and test whether it is created successfully
    '''
    
    # register for new users
    newUser1 = auth_register('z5237609@unsw.edu.au', 'Zxl471238986', 'Matty', 'Zhang')
    newUser1_id = newUser1['u_id']
    newUser1_token = newUser1['token'] 
    
    # create a channel
    newChannel = channels_create(newUser1_token, 'General', True)
    channel_ID = newChannel['channel_id']
    
    # list all the channels 
    channelsReturn = channels_listall(newUser1_token)
    
    # checking
    assert len(channelsReturn) == 1
    assert channelsReturn['channels'][0]['channel_id'] == channel_ID
    
def test_channels_create_case2():

    '''
    two users create a public and a private channel and 
    test whether they are created successfully
    '''
    
    # register for new users
    newUser2 = auth_register('z1234567@unsw.edu.au', 'Zfheiu3H33', 'Foster', 'Chen')
    newUser2_id = newUser2['u_id']
    newUser2_token = newUser2['token']   

    newUser4 = auth_register('z1344327@unsw.edu.au', 'fdgrweUY32', 'Fos', 'Che')
    newUser4_id = newUser4['u_id']
    newUser4_token = newUser4['token'] 
    
    # create two channels (one public and one private)
    newChannel1 = channels_create(newUser2_token, 'General', True)
    channel_ID1 = newChannel1['channel_id']

    newChannel2 = channels_create(newUser4_token, 'Random', False)
    channel_ID2 = newChannel2['channel_id']
        
    # list all the channels 
    channelsReturn1 = channels_listall(newUser2_token)
    
    # checking
    assert len(channelsReturn1) == 2
    assert channelsReturn1['channels'][0]['channel_id'] == channel_ID1
    assert channelsReturn1['channels'][1]['channel_id'] == channel_ID2
            
def test_channels_create_inputError():
    
    '''
    when the length of the channel name is more than 20 characters, inputerror raises.
    '''
    
    # register for a new user
    newUser3 = auth_register('z7654321@unsw.edu.au', 'dhf4830ZH6', 'First', 'Last')
    newUser3_id = newUser3['u_id']
    newUser3_token = newUser3['token']
    
    # create a channel (inputerror)
    with pytest.raises(InputError):
        channels_create(newUser3_token, 'GeneralGeneralGeneral', True)
