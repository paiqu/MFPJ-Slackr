import pytest
from auth import auth_register
from user import user_profile_sethandle, user_profile
from error import InputError

'''
This is a test file for user_profile function

InputError: User with u_id is not a valid user

1. test for normal case 
    (For a valid user, returns information about 
    their email, first name, last name, and handle)
    
2. test for InputError
    when user with u_id is not a valid user
'''

def test_user_profile():
    
    # register for a new user
    newUser1 = auth_register('z5237609@unsw.edu.au', 'Zxl471238986', 'Matty', 'Zhang')
    newUser1_id = newUser1['u_id']
    newUser1_token = newUser1['token']
    
    # give a handle name to user
    user_profile_sethandle(newUser1_token, 'MattyLei')
    
    returnUser1 = user_profile(newUser1_token, newUser1_id)
    
    # get my return value
    returnUser1_email = returnUser1['email']
    returnUser1_first = returnUser1['name_first']
    returnUser1_last = returnUser1['name_last']  
    returnUser1_handle = returnUser1['handle_str']
    
    # check whether they are same
    assert returnUser1_email == 'z5237609@unsw.edu.au'
    assert returnUser1_first == 'Matty'
    assert returnUser1_last == 'Zhang'
    assert returnUser1_handle == 'MattyLei'
    
def test_user_profile_inputError():

    # register for a new user
    newUser2 = auth_register('z1234567@unsw.edu.au', 'dfdsbuS123', 'Haofu', 'Chen')
    newUser2_id = newUser2['u_id']
    newUser2_token = newUser2['token']
          
    with pytest.raises(InputError):
        user_profile(newUser2_token, newUser2_id + 4)
    

