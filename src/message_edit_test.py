import pytest
from auth import auth_register 
from error import AccessError
from message import message_send, message_edit
from channels import channels_create
from channel import channel_messages, channel_details, channel_invite

   
def test_message_edit():
    '''
    tests:
    1. update with new texts
    2. update with empty string, which will delete the msg
    '''
    user01 = auth_register('z123456@unsw.edu.au', 'ajsd123asd123', 'first_name', 'surname')
    user01_token = user01['token']
    
    channel01 = channels_create(user01_token, 'General', True)
    channel01_id = channel01['channel_id']
    
    msg = message_send(user01_token, channel01_id, 'to be edited')
    msg_id = msg['message_id']
        
    # 1. update with new text
    message_edit(user01_token, msg_id, 'has been edited')

    chan_msg = channel_messages(user01_token, channel01_id, 0)
    edited_msg = chan_msg['messages'][0]['message']
    assert(edited_msg == 'has been edited')
    
    # 2. update with empty string, which will delete message_edit
    message_edit(user01_token, msg_id, '')
    msg_end = chan_msg['end']
    assert msg_end == -1

    
def test_message_edit_by_owner():
    # test: messages sent by members can be edited by owner of this channel
    user01 = auth_register('z123456@unsw.edu.au', 'ajsd123asd123', 'first_name', 'surname')
    user01_token = user01['token']
    
    user02 = auth_register('z74588324@unsw.edu.au', 'ajsd123asd123', 'coco', 'S')
    user02_token = user02['token']
    
    channel01 = channels_create(user01_token, 'General', True)
    channel01_id = channel01['channel_id']
    
    # user02 sent message
    msg = message_send(user02_token, channel01_id, 'to be edited')
    msg_id = msg['message_id']
    
    # owner: user01 try to edit
    message_edit(user01_token, msg_id, 'has been edited')
    
    chan_msg = channel_messages(user01_token, channel01_id, 0)
    edited_msg = chan_msg['messages'][0]['message']
    assert(edited_msg == 'has been edited')

def test_message_edit_AccessError_edited_by_unauthorised_user ():
    # testing one member try to edit other's message
    user01 = auth_register('z123456@unsw.edu.au', 'ajsd123asd123', 'tom', 'L')
    user01_id = user01['u_id']
    user01_token = user01['token']  
    
    user02 = auth_register('z9877654@unsw.edu.au', 'ajsd123asd123', 'tony', 'T')
    user02_id = user02['u_id']
    user02_token = user02['token']  
     
    channel01 = channels_create(user01_token, 'General', True)
    channel01_id = channel01['channel_id']
    
    msg = message_send(user01_token, channel01_id, 'to be edited')
    msg_id = msg['message_id']
      
    with pytest.raises(AccessError) as e:
        # edited by user02, but this message was sent by use01 
        message_edit(user02_token, msg_id, 'has been edited')
    
    
def test_message_edit_AccessError_no_owner():
    # testing not owner try to edit other member's message
    user01 = auth_register('z123456@unsw.edu.au', 'ajsd123asd123', 'tom', 'L')
    user01_id = user01['u_id']
    user01_token = user01['token']  
    
    user02 = auth_register('z9877654@unsw.edu.au', 'ajsd123asd123', 'tony', 'T')
    user02_id = user02['u_id']
    user02_token = user02['token']  
     
    channel01 = channels_create(user01_token, 'General', True)
    channel01_id = channel01['channel_id']
    
    msg = message_send(user01_token, channel01_id, 'to be edited')
    msg_id = msg['message_id']
        
    with pytest.raises(AccessError) as e:
        # editer by not admin or not ower of channel
        message_edit(user02_token, msg_id, 'has been edited')
        
