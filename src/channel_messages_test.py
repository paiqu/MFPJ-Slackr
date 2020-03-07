import pytest
from error import InputError, AccessError 
from auth import auth_register 
from channels import channels_create
from channel import channel_messages
from message import message_send

'''
    check the messages's id is the same and since this channel doesn't
    have more than 50 messages, check '-1' is return in "end"
'''

def test_channel_messages():
    user01 = auth_register('z1234567@ad.unsw.edu.au', 'password12345', 'name', 'surname')
    user01_id = user01['u_id']
    user01_token = user01['token']
    
    channel_01 = channels_create(user01_token, 'General', True)
    channel_01_id = channel01['channel_id']
    
    # sending messages
    msg01_id = message_send(user01_token, channel_01_id, 'testing message 1')['message_id']
    msg02_id = message_send(user01_token, channel_01_id, 'testing message 2')['message_id']   
    msg03_id = message_send(user01_token, channel_01_id, 'testing message 3')['message_id'] 
    
    # get channel messages
    chan_msg = channel_messages(user01_token, channel_01_id, 0)
    most_recent_msg_id = chan_msg['messages'][0]['message_id']
    second_msg_id = chan_msg['messages'][1]['message_id']
    first_sent_mgs_id = chan_msg['messages'][2]['message_id']
    end_return = chan_msg['end']
    
    assert(most_recent_msg_id == msg03_id)
    assert(second_msg_id == msg02_id)
    assert(first_sent_mgs_id == msg01_id)
    assert(end_return == -1)
    
    # when the numbers of messages reach 50, get the return value in 'end'
    for i in range(1,51):
        message_send(user01_token, channel_01_id, 'testing message')
        
    end_return = channel_messages(user01_token, channel_01_id, 0)['end']
    assert(end_return == 50)
    
 
def test_channel_messages_InputError():
    user01 = auth_register('z1234567@ad.unsw.edu.au', 'password12345', 'name', 'surname')
    user01_id = user01['u_id']
    user01_token = user01['token']
    
    channel_01 = channels_create(user01_token, 'General', True)
    channel_01_id = channel01['channel_id']
    
    msg01_id = message_send(user01_token, channel_01_id, 'testing message 1')['message_id']
    
    # Channel ID is not a valid channel
    with pytest.raises(InputError) as e:
        channel_messages(user01_token, channel_01_id + 10, 0)
        
    # start is greater than the total number of messages in the channel
    with pytest.raises(InputError) as e:
        channel_messages(user01_token, channel_01_id, 10)

def test_channel_messages_AccessError():   
    user01 = auth_register('z1234567@ad.unsw.edu.au', 'password12345', 'name', 'surname')
    user01_token = user01['token']
    
    user02 = auth_register('z8998996@ad.unsw.edu.au', 'password12345', 'name', 'surname')
    user02_token = user02['token']
    
    
    channel_01 = channels_create(user01_token, 'General', True)
    channel_01_id = channel01['channel_id']
    
    msg01_id = message_send(user01_token, channel_01_id, 'testing message 1')['message_id']
    
    # Authorised user is not a member of channel with channel_id
    with pytest.raises(AccessError) as e:
        channel_messages(user02_token, channel_01_id, 0)
