import pytest
from auth import auth_register 
from error import AccessError
from message import message_send, message_edit
from channels import channels_create
from channel import channel_messages, channel_details

'''
AccessError when none of the following are true:
    - Message with message_id was sent by the authorised user making this request
    - The authorised user is an admin or owner of this channel or the slackr
''' 

   
def test_message_edit():
    user01 = auth_register('z123456@unsw.edu.au', 'ajsd123asd123', 'first_name', 'surname')
    user01_id = user01['u_id']
    user01_token = user01['token']
    
    channel01 = channels_create(user01_token, 'General', True)
    channel01_id = channel01['channel_id']
    
    msg = message_send(user01_token, channel01_id, 'to be edited')
    msg_id = msg['message_id']
        
    # test: update with new text
    message_edit(user01_token, msg_id, 'has been edited')

    chan_msg = channel_messages(user01_token, channel01_id, 0)
    edited_msg = chan_msg['messages'][0]['message']
    assert(edited_msg == 'has been edited')
    
    # test: update with empty string, which will delete message_edit
    message_edit(user01_token, msg_id, '')
    msg_end = chan_msg['end']
    assert(mss_end == -1)

def test_message_edit_AccessError():
    user01 = auth_register('z123456@unsw.edu.au', 'ajsd123asd123', 'first_name', 'surname')
    user01_id = user01['u_id']
    user01_token = user01['token']  
    
    user02 = auth_register('z9877654@unsw.edu.au', 'ajsd123asd123', 'family_name', 'last_name')
    user02_id = user02['u_id']
    user02_token = user02['token']  
     
    channel01 = channels_create(user01_token, 'General', True)
    channel01_id = channel01['channel_id']
    
    msg = message_send(user01_token, channel01_id, 'to be edited')
    msg_id = msg['message_id']
      
    with pytest.raises(AccessError) as e:
        # edited by unauthorised user 
        message_edit(user02_token, msg_id, 'has been edited')
        
    with pytest.raises(AccessError) as e:
        # editer by not admin or not ower of channel
        message_edit(user02_token, msg_id, 'has been edited')
        
