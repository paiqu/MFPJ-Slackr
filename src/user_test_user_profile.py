import pytest
from auth import auth_register
from user import user_profile_sethandle, user_profile
'''
This is a test file for user_profile function

InputError: User with u_id is not a valid user

1. test for normal case 
    (For a valid user, returns information about 
    their email, first name, last name, and handle)
    
2. test for InputError
'''

def test_user_profile():
    
    # register for a new user
    newUser = auth_register('z5237609@unsw.edu.au', 'Zxl471238986', 'Matty', 'Zhang')
    newUser_id = newUser['u_id']
    newUser_token = newUser['token']
    
    # give a handle name to user
    user_profile_sethandle(newUser_token, 'MattyLei')
    
    returnUser = user_profile(newUser_token, newUser_id)
    
    # get my return value
    returnUser_email = returnUser['email']
    returnUser_first = returnUser['name_first']
    returnUser_last = returnUser['name_last']  
    returnUser_handle = returnUser['handle_str']
    
    # check whether they are same
    assert returnUser_email == 'z5237609@unsw.edu.au'
    assert returnUser_first == 'Matty'
    assert returnUser_last == 'Zhang'
    assert returnUser_handle == 'MattyLei'
