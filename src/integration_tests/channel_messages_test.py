import pytest
from error import InputError, AccessError 
from auth import auth_register 
from channels import channels_create
from channel import channel_messages
from message import message_send


def test_channel_messages():
    '''
    tests: 
    1. sent 3 msgs and check the order and msg_id of returned msgs
    2. only 3 msgs, check it returns "-1" in "end"
    3. sent 50 more msgs and use "0" as "start" to run, check it returns "50" in "end"
    4. sent 50 more msgs and use "50" as "start" to run, check it returns "100" in "end"
    '''
    # create user
    user01 = auth_register('z1234567@ad.unsw.edu.au', 'password12345', 'name', 'surname')
    user01_id = user01['u_id']
    user01_token = user01['token']
    
    # create channel
    channel_01 = channels_create(user01_token, 'General', True)
    channel_01_id = channel_01['channel_id']
    
    # 1. sending 3 messages
    msg01_id = message_send(user01_token, channel_01_id, 'testing message 1')['message_id']
    msg02_id = message_send(user01_token, channel_01_id, 'testing message 2')['message_id']   
    msg03_id = message_send(user01_token, channel_01_id, 'testing message 3')['message_id'] 
    
    # 1. get channel messages and the id
    chan_msg = channel_messages(user01_token, channel_01_id, 0)
    most_recent_msg_id = chan_msg['messages'][0]['message_id']
    second_msg_id = chan_msg['messages'][1]['message_id']
    first_sent_mgs_id = chan_msg['messages'][2]['message_id']
    end_return = chan_msg['end']
    
    # 1. check the messages's id are matched
    assert most_recent_msg_id == msg03_id
    assert second_msg_id == msg02_id 
    assert first_sent_mgs_id == msg01_id 
    
    # 2. only 3 msgs, check '-1' is return in "end"
    assert end_return == -1 
    
    # 3. when the numbers of messages reach 50, get the return value in 'end'
    for i in range(1,51):
        message_send(user01_token, channel_01_id, 'testing message')
        
    end_return = channel_messages(user01_token, channel_01_id, 0)['end']
    assert end_return == 50
    
    # 4. if the 'start' is 50, check it returns 100 in "end" or not 
    for i in range(1,60):
        message_send(user01_token, channel_01_id, 'testing message')

    end_return = channel_messages(user01_token, channel_01_id, 50)['end']
    assert end_return == 100
 
def test_channel_messages_InputError_invalid_channel():
    # test: when channel ID is not a valid channel
    user01 = auth_register('z1234567@ad.unsw.edu.au', 'password12345', 'name', 'surname')
    user01_id = user01['u_id']
    user01_token = user01['token']
    
    channel_01 = channels_create(user01_token, 'General', True)
    channel_01_id = channel_01['channel_id']
    
    msg01_id = message_send(user01_token, channel_01_id, 'testing message 1')['message_id']
    
    with pytest.raises(InputError) as e:
        channel_messages(user01_token, channel_01_id + 10, 0)
        
    
def test_channel_messages_InputError_invalid_start():
    # test: 'start' is greater than the total number of messages in the channel
    user01 = auth_register('z1234567@ad.unsw.edu.au', 'password12345', 'name', 'surname')
    user01_id = user01['u_id']
    user01_token = user01['token']
    
    channel_01 = channels_create(user01_token, 'General', True)
    channel_01_id = channel_01['channel_id']
    
    msg01_id = message_send(user01_token, channel_01_id, 'testing message 1')['message_id']    
    
    with pytest.raises(InputError) as e:
        channel_messages(user01_token, channel_01_id, 10)

def test_channel_messages_AccessError_no_in_channel():
    # test: Authorised user is not a member of channel with channel_id    
    user01 = auth_register('z1234567@ad.unsw.edu.au', 'password12345', 'name', 'surname')
    user01_token = user01['token']
    
    user02 = auth_register('z8998996@ad.unsw.edu.au', 'password12345', 'nana', 'su')
    user02_token = user02['token']
    
    
    channel_01 = channels_create(user01_token, 'General', True)
    channel_01_id = channel_01['channel_id']
    
    msg01_id = message_send(user01_token, channel_01_id, 'testing message 1')['message_id']
    
    # user02 is not a member of channel_01
    with pytest.raises(AccessError) as e:
        channel_messages(user02_token, channel_01_id, 0)