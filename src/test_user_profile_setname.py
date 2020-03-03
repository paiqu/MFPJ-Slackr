import pytest
from user import user_profile, user_profile_setname
from auth import auth_register 
from error import InputError

"""
InputError:
name_first is not between 1 and 50 characters
name_last is not between 1 and 50 characters
"""
#This function is to test the name_first between 1 and 50 
def test_user_inputError_one():
    user_one = auth_register("timmy123@icloud.com", "TimmyLiew", "Timmy", "Liew")
    user_id_one = user_one["u_id"]
    token_one = user_one["token"]
#if name_first is greater than 50->InputError     
    with pytest.raise(InputError)
        user_profile_setname(token_one,'a' * 1000)
#This function is to test the name_last between 1 and 50  
def test_user_inputError_two():
    user_two = auth_register("Ivan@icloud.com", "Ivanxxx", "Ivan", "Liew")
    user_id_two = uesr_two["u_id"]
    token_two = user_two["token"]
#if name_last is greater than 50->InputError 
    with pytest.raise(InputError)
        user_profile_setname(token_two,'a' * 1000)    
