import pytest
from user import user_profile, users_all
from auth import auth_register
"""
Test return the correct list of users and informations
"""
#This function is to test the normal case to return correct informations
def test_users_all_success():
#create a new user 
    user_one = auth_register('z123456@unsw.edu.au', 'z123456', 'Honey', 'Pii')
    user_one_id = user_one["u_id"]
    token_one = user_one["token"]
    
    return_user_one = user_profile(token_one, user_one_id)

    # store the return value
    return_one_email = return_user_one["email"]
    return_one_first_name = return_user_one["name_first"]
    return_one_last_name = return_user_one["name_last"]  

    # check whether they are same
    assert return_one_email == 'z123456@unsw.edu.au'
    assert return_one_first_name == 'Honey'
    assert return_one_last_name == 'Pii'



    


    

    
