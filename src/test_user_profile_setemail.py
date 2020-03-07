import pytest
import re
from user import user_profile, user_profile_setemail
from auth import auth_register 
from error import InputError
"""
Input Error:
The first case:Email entered is not valid;

The second case:Email entered is already used by another user;

First, testing the successful case when the user entered the correct format of email,
and the testing the Email entered is not valid, the last for testing the repeated case  
"""
    #This function test the successful case when user type the right format email
def test_user_success():
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'    
    #create the user    
    user_zero = auth_register("hello123@icloud.com", "Helloihhvh", "Jaky", "Chan")
    user_id_zero = user_zero["u_id"]
    token_zero = user_zero["token"]
    #check whether the email format is correct   
    assert(re.search(regex,user_profile_setemail) == True)
        
    #This function is to test the first case 
def test_user_inputError_one():
    #create the user
    user_one = auth_register("timmy123@icloud.com", "TimmyLiew", "Timmy", "Liew")
    user_id_one = user_one["u_id"]
    token_one = user_one["token"]
    #if the user entered the invalid email->InputError
    with pytest.raises(InputError):
        user_profile_setemail(token_one,'ctrressh456.com')

    #This function is to test the second case
def test_user_inputError_two():
    #create the user
    user_two = auth_register("Ivan@icloud.com", "Ivanxxx", "Ivan", "Liew")
    user_id_two = user_two["u_id"]
    token_two = user_two["token"]
    #create the another user    
    user_three = auth_register("Lena@icloud.com", "Fvshhc", "Lena", "Liew") 
    user_id_three = user_three["u_id"]
    token_three = user_three["token"]
    #When the user use another user's email->InputError
    with pytest.raises(InputError):
        user_profile_setemail(token_three,'Ivan@icloud.com')   

