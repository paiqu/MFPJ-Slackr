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
    
    '''
    a normal case test (two users)(one user updates profile)
    '''
    
    # register for new users
    newUser1 = auth_register('z5237609@unsw.edu.au', 'Zxl471238986', 'Matty', 'Zhang')
    newUser1_id = newUser1['u_id']
    newUser1_token = newUser1['token']

    newUser2 = auth_register('z1234567@unsw.edu.au', 'dfdsbuS123', 'Haofu', 'Chen')
    newUser2_id = newUser2['u_id']
    newUser2_token = newUser2['token']
        
    # update a handle name to user 1
    user_profile_sethandle(newUser1_token, 'MattyLei')
    
    # get user_profile
    returnUser1 = user_profile(newUser1_token, newUser1_id)
    returnUser2 = user_profile(newUser2_token, newUser2_id)
        
    # get my return value
    returnUser1_email = returnUser1['user']['email']
    returnUser1_first = returnUser1['user']['name_first']
    returnUser1_last = returnUser1['user']['name_last']
    returnUser1_handle = returnUser1['user']['handle_str']
    
    returnUser2_email = returnUser2['user']['email']
    returnUser2_first = returnUser2['user']['name_first']
    returnUser2_last = returnUser2['user']['name_last']
    returnUser2_handle = returnUser2['user']['handle_str']
       
    # check whether they are same
    assert returnUser1_email == 'z5237609@unsw.edu.au'
    assert returnUser1_first == 'Matty'
    assert returnUser1_last == 'Zhang'
    assert returnUser1_handle == 'MattyLei'

    assert returnUser2_email == 'z1234567@unsw.edu.au'
    assert returnUser2_first == 'Haofu'
    assert returnUser2_last == 'Chen'
    assert returnUser2_handle == 'haofuchen'
  
def test_user_profile_inputError():

    '''
    test for the inputError case when user Id is invalid.
    '''

    # register for a new user 2
    newUser = auth_register('z1234567@unsw.edu.au', 'dfdsbuS123', 'Haofu', 'Chen')
    newUser_id = newUser['u_id']
    newUser_token = newUser['token']
    
    # test Inputerror (wrong user ID)
    with pytest.raises(InputError):
        user_profile(newUser_token, newUser_id + 4)
    

