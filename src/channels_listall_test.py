import pytest
from auth import auth_register 
from channels import channels_create,channels_listall
from channel import channel_invite

'''
Two users create  two channels separately, and call this function to check whether it returns all channels even it takes only one user's token
'''

def test_channels_list():
    user01 = auth_register('z123456@unsw.edu.au', 'ajsd123asd123', 'first_name', 'surname')
    user01_id = user01['u_id']
    user01_token = user01['token']  
    
    user02 = auth_register('z9877654@unsw.edu.au', 'ajsd123asd123', 'family_name', 'last_name')
    user02_id = user02['u_id']
    user02_token = user02['token']  
    
    # user01 create channel01 and user02 create channel02
    channel01 = channels_create(user01_token, 'General', True)
    channel01_id = channel01['channel_id']
    channel02 = channels_create(user02_token, 'General', True)
    channel02_id = channel02['channel_id']
    
    
    chan_list_02 = channels_listall(user02_token)
    chan_list_02_id01 = chan_list_01['channels'][0]['channel_id']
    chan_list_02_id02 = chan_list_01['channels'][1]['channel_id']
    
    # check channels_listall return both channel01_id and channel02_id
    assert(chan_list_02_id01 == channel01_id or chan_list_02_id01 == channel02_id)
    assert(chan_list_02_id02 == channel01_id or chan_list_02_id02 == channel02_id)
