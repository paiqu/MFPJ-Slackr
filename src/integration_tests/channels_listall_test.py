import pytest
from auth import auth_register 
from channels import channels_create,channels_listall
from channel import channel_invite

def test_channels_list():
    '''
    tests: returns all channels despite whether a selected member is apart of or not
    '''
    user01 = auth_register('z123456@unsw.edu.au', 'ajsd123asd123', 'first_name', 'surname')
    user01_id = user01['u_id']
    user01_token = user01['token']  
    
    user02 = auth_register('z9877654@unsw.edu.au', 'ajsd123asd123', 'tami', 'Li')
    user02_id = user02['u_id']
    user02_token = user02['token']  
    
    user03 = auth_register('z3242312@unsw.edu.au', 'ajsd123asd123', 'tom', 'SM')
    user03_id = user03['u_id']
    user03_token = user03['token']
    
    # user01 create channel01
    channel01 = channels_create(user01_token, 'channel1', True)
    channel01_id = channel01['channel_id']
    # user02 create channel02 and channel03
    channel02 = channels_create(user02_token, 'channel2', True)
    channel02_id = channel02['channel_id']
    channel03 = channels_create(user02_token, 'channel3', True)
    channel03_id = channel03['channel_id']
    # user03 create channel04
    channel04 = channels_create(user03_token, 'channel4', True)
    channel04_id = channel04['channel_id']
    
    # get the id of channels using channels_listall
    chan_list_01 = channels_listall(user01_token)
    chan_list_id01 = chan_list_01['channels'][0]['channel_id']
    chan_list_id02 = chan_list_01['channels'][1]['channel_id']
    chan_list_id03 = chan_list_01['channels'][2]['channel_id']
    chan_list_id04 = chan_list_01['channels'][3]['channel_id']
    
    # check channels_listall return all channels
    assert chan_list_id01 == channel01_id
    assert chan_list_id02 == channel02_id
    assert chan_list_id03 == channel03_id
    assert chan_list_id04 == channel04_id
    
    # pass another user_token and check its return again 
    chan_list_02 = channels_listall(user02_token)
    chan_list_id05 = chan_list_02['channels'][0]['channel_id']
    chan_list_id06 = chan_list_02['channels'][1]['channel_id']
    chan_list_id07 = chan_list_02['channels'][2]['channel_id']
    chan_list_id08 = chan_list_02['channels'][3]['channel_id']
    
    assert chan_list_id05 == channel01_id
    assert chan_list_id06 == channel02_id
    assert chan_list_id07 == channel03_id
    assert chan_list_id08 == channel04_id
