import pytest
from user import user_profile, user_profile_setname
from auth import auth_register 
from error import InputError

"""
Test the one user and two user;

InputError:
name_first is not between 1 and 50 characters
name_last is not between 1 and 50 characters
"""
    #This function is to test the normal case for one user that wanna change the name
def test_user_success_one():
    
    #register a user
    user_zero = auth_register('z5237543@unsw.edu.au', 'z645326', 'Coco', 'Halo')
    user_id_zero = user_zero['u_id']
    token_zero = user_zero['token']
    
    #check whether the user name_first and name_last update
    user_profile_setname(token_zero,'Jelly','Peloo')
    
    user_dict = user_profile(token_zero, user_id_zero)
    assert user_dict['user']['name_first'] == 'Jelly'
    assert user_dict['user']['name_last'] == 'Peloo'
    
    #This function is to test two user when one user wanna change the name
def test_user_success_two():
    
    #register first user
    user_zero = auth_register('z5236543@unsw.edu.au', 'z63445326', 'Cc', 'Hooo')
    user_id_zero = user_zero['u_id']
    token_zero = user_zero['token']
    
    #register second user
    user_one = auth_register('z4737543@unsw.edu.au', 'z54626326', 'OO', 'Coco')
    user_id_one = user_one['u_id']
    token_one = user_one["token"]
    
    #check whether the second user has changed the name_first
    user_profile_setname(token_one,'Tree','Pual')
    
    user_dict = user_profile(token_one, user_id_one)
    assert user_dict['user']['name_first'] == 'Tree'
    assert user_dict['user']['name_last'] == 'Pual'
    
    #This function will test when both two users wanna change the name
def test_user_success_three():

    #register first user
    user_zero = auth_register('z8654343@unsw.edu.au', 'z7456783326', 'Nuu', 'Puu')
    user_id_zero = user_zero['u_id']
    token_zero = user_zero['token']
    
    #register second user
    user_one = auth_register('z4737632@unsw.edu.au', 'z54tury326', 'Haham', 'Ham')
    user_id_one = user_one['u_id']
    token_one = user_one['token']
    
    user_profile_setname(token_zero,'Youy','Tyre')
    user_profile_setname(token_one,'Hbhd','Gil')
    
    user_dict = user_profile(token_zero, user_id_zero)
    user_dict_two = user_profile(token_one, user_id_one)
    
    assert user_dict['user']['name_first'] == 'Youy'
    assert user_dict['user']['name_last'] == 'Tyre'
    assert user_dict_two['user']['name_first'] == 'Hbhd'
    assert user_dict_two['user']['name_last'] == 'Gil'
           
    #This function is to test the name_first between 1 and 50 
def test_user_inputError_one():
    
    #register a user
    user_one = auth_register('z6742677@unsw.edu.au', 'tirbwbhT', 'Timmy', 'Liew')
    user_id_one = user_one['u_id']
    token_one = user_one['token']
    
    #if name_first and name_last is greater than 50->InputError     
    with pytest.raises(InputError):
        user_profile_setname(token_one,'a' * 1000, 'b' * 1000)
 
