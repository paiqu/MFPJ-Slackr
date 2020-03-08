import pytest
from auth import auth_register 
from channels import channels_create, channels_list
from channel import channel_invite


'''
Provide a list of all channels (and their associated details) that the authorised user is part of
    1. user is the owner
    2. user is a member   
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
    
    # and user02 invite user01 into channel02
    channel_invite(user01_token, channel02_id, user01_id)
    
    chan_list_01 = channels_list(user01_token)
    chan_list_01_id01 = chan_list_01['channels'][0]['channel_id']
    chan_list_01_id02 = chan_list_01['channels'][1]['channel_id']
    
    # check user01's channel_id is the same as channel01_id and channel02_id
    assert(chan_list_01_id01 == channel01_id or chan_list_01_id01 == channel02_id)
    assert(chan_list_01_id02 == channel01_id or chan_list_01_id02 == channel02_id)
