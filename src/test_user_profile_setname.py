import pytest
from user import user_profile, user_profile_setname
from auth import auth_register 
from error import InputError

"""
Test the normal case;

InputError:
name_first is not between 1 and 50 characters
name_last is not between 1 and 50 characters
"""
    #This function is to test the normal case
def test_user_success():
    
    #register a user
    user_zero = auth_register("z5237543@unsw.edu.au", "z645326", "Coco", "Halo")
    user_id_zero = user_zero["u_id"]
    token_zero = user_zero["token"]
    
    #check whether the user name_first and name_last update
    user_dict = user_profile(token_zero, 'u_id')
    assert user_dict['user']['name_first'] == 'Coco'
    assert user_dict['user']['name_last'] == 'Halo'
    
    #This function is to test the name_first between 1 and 50 
def test_user_inputError_one():
    
    #register a user
    user_one = auth_register("timmy123@icloud.com", "TimmyLiew", "Timmy", "Liew")
    user_id_one = user_one["u_id"]
    token_one = user_one["token"]
    
    #if name_first and name_last is greater than 50->InputError     
    with pytest.raises(InputError):
        user_profile_setname(token_one,'a' * 1000, 'b' * 1000)
 
