import pytest

from channel import channel_invite, channel_details, channel_messages 
from auth import auth_login, auth_register, auth_logout 
from channels import channels_create

from error import InputError, AccessError
##fixture

@pytest.fixture 

def test_channel_details_correct():
    """
    This test performs a test on the channel_details function . This test is correct.
    """
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    user1_token = user1['token']

    user2= auth_register('MFPJ@unsw.edu.au','!987bye', 'Student', 'Test')
    u_id2=user2['u_id']
    user2_token = user2['token']

    channel1 = channels_create(user1_token, 'Channel_MFPJ', True)
    c_id1=channel1['channel_id']
    
    
    channel_invite(user1_token, c_id1,u_id2)
    
    
    assert channel_details(user1_token, c_id1) == {
        'name' : 'Channel1',
        'owner_members': { { u_id: u_id1, 
                            name_first: user1[name_first],
                            name_last: user1[name_last]},
        }
        
        'all_members':  { { u_id: u_id1, 
                            name_first: user1[name_first],
                            name_last: user1[name_last]},
                          { u_id: u_id2, 
                            name_first: user2[name_first],
                            name_last: user2[name_last]},
        }
    }    

def test_invalid_channelID():
    """
    Channel ID is not a valid channel
    """

    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    user1_token = user1['token']

    user2= auth_register('MFPJ@unsw.edu.au','!987bye', 'Student', 'Test')
    u_id2=user2['u_id']
    user2_token = user2['token']

    channel1 = channels_create(user1_token, 'Channel_MFPJ', True)
    c_id1=channel1['channel_id']

    Invalid_ChannelID = 8888
    
    
    channel_invite(user1_token, c_id1,u_id2)

    with pytest.raises(AccessError) as e:
        channel_details(user1_token, Invalid_ChannelID)

    
def test_nonmember_asks_details():
    '''
    A user who is not part of a channel himself, is not allowed to ask details about that channel 
    I.e. A user must be a member of the channel themselves before requesting channel details 
    '''   
    user1 = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    u_id1=user1['u_id']
    user1_token = user1['token']

    user2= auth_register('MFPJ@unsw.edu.au','!987bye', 'Student', 'Test')
    u_id2=user2['u_id']
    user2_token = user2['token']
    
    user3 = auth_register('git@unsw.edu.au','!987password', 'Jane', 'Smith')
    u_id3=user3['u_id']
    user3_token = user3['token']
    
    Invalid_User = 9999

    channel1 = channels_create(user1_token, 'Channel1', True)
    c_id1=channel1['channel_id']
    
    
    with pytest.raises(InputError) as e:
        channel_details(user3_token, c_id1)
    
        