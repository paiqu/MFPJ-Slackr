import pytest
from user import user_profile, user_profile_sethandle
from auth import auth_register 
from error import InputError

"""
InputError:
The first case:handle string entered between 3 and 20 character
The second case: handle string entered is already used
"""
#This function is to test the first case
def test_user_handle_inputError_one():
#create the user
    user_one = auth_register("timm123@icloud.com", "TimmLiew", "Timm", "Li")
    user_id_one = user_one["u_id"]
    token_one = user_one["token"]
#if the user entered out of 20 character->InputError
    with pytest.raises(InputError):
        user_profile_sethandle(token_one,'a' * 1000)
#if the user entered between 0 and 2->InputError
    with pytest.raises(InputError):
        user_profile_sethandle(token_one,'b' * 2)    


#This function is to test teh second case
def test_user_handle_inputError_two():
#create the user
    user_two = auth_register("timm3@icloud.com", "TiLiw", "Taammaaaaa", "Aaaaaa")
    user_id_two = user_two["u_id"]
    user_two_handle = user_two["handle"]
    token_two = user_two["token"]
#create the another user
    user_three = auth_register("timasdm123@icloud.com", "TimdsmLiew", "Dandmm", "Lmi")
    user_id_three = user_three["u_id"]
    token_three = user_three["token"]
#if handle string is already existed->InputError
    with pytest.raises(InputError):
        user_profile_sethandle(token_three,'handle')
    
    
