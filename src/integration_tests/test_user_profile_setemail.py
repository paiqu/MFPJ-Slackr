import pytest
import re
from user import user_profile, user_profile_setemail
from auth import auth_register 
from error import InputError
"""
Input Error:
The first case:Email entered is not valid;

The second case:Email entered is already used by another user;

First, testing the successful case when the one or two users entered the correct format of email,
and the testing the Email entered is not valid, the last for testing the repeated case  
"""
    #This function test the successful case when one user set the email
def test_user_success_one():
        
    #create the user    
    user_zero = auth_register('z6745462@unsw.edu.au', 'Helloihhvh', 'Jaky', 'Chan')
    user_id_zero = user_zero['u_id']
    token_zero = user_zero['token']
    
    #set the new email
    user_profile_setemail(token_zero,'z6543217@unsw.edu.au')   
    
    #check whether the email can be setted
    user_dict = user_profile(token_zero, user_id_zero)
    assert user_dict['user']['email'] == 'z6543217@unsw.edu.au'

    #This function will test the successful case when two users set the email
def test_user_success_two():
    
    #create the user    
    user_zero = auth_register('z6744562@unsw.edu.au', 'Hehhvh', 'Jakey', 'Chinn')
    user_id_zero = user_zero['u_id']
    token_zero = user_zero['token']
    
    #create the user    
    user_first = auth_register('z7645462@unsw.edu.au', 'Health', 'Jyru', 'Tenn')
    user_id_first = user_first['u_id']
    token_first = user_first['token']     
    
    #set the new email for user one
    user_profile_setemail(token_zero,'z1237654@unsw.edu.au')
    
    #set the new email for user two
    user_profile_setemail(token_first,'z9812347@unsw.edu.au')
    
    #check whether the email can be setted
    user_dict = user_profile(token_zero, user_id_zero)
    user_dict_two = user_profile(token_first, user_id_first)
    assert user_dict ['user']['email'] == 'z1237654@unsw.edu.au'
    assert user_dict_two ['user']['email'] == 'z9812347@unsw.edu.au'
    
    #This function is to test the first case 
def test_user_inputError_one():
    
    #create the user
    user_one = auth_register('z5674897@unsw.edu.au', 'TimmyLiew', 'Timmy', 'Liew')
    user_id_one = user_one['u_id']
    token_one = user_one['token']
    
    #if the user entered the invalid email->InputError
    with pytest.raises(InputError):
        user_profile_setemail(token_one,'ctrressh456.com')


    #This function is to test the second case
def test_user_inputError_two():
    
    #create the user
    user_two = auth_register('z5467367@unsw.edu.au', 'Ivanxxx', 'Ivan', 'Liew')
    user_id_two = user_two['u_id']
    token_two = user_two['token']
    
    #create the another user    
    user_three = auth_register('z5857675@unsw.edu.au', 'Fvshhc', 'Lena', 'Liew') 
    user_id_three = user_three['u_id']
    token_three = user_three['token']
    
    #When the user use another user's email->InputError
    with pytest.raises(InputError):
        user_profile_setemail(token_three,'z5467367@unsw.edu.au')   

