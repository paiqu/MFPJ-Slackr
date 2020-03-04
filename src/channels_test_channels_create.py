import pytest
from auth import auth_register
from error import InputError
from channels import channels_create

'''
This is a test file for channels_create function

InputError: name is more than 20 characters long

1. test for normal case 
    (Creates a new channel with that name 
    that is either a public or private channel)
    
2. test for InputError
    when name is more than 20 characters long
'''

def test_user_profile():
    
    # register for a new user
    newUser1 = auth_register('z5237609@unsw.edu.au', 'Zxl471238986', 'Matty', 'Zhang')
    newUser1_id = newUser1['u_id']
    newUser1_token = newUser1['token']

def test_user_profile_inputError():
    
    # register for a new user
    newUser3 = auth_register('z7654321@unsw.edu.au', 'dhf4830ZH6', 'First', 'Last')
    newUser3_id = newUser3['u_id']
    newUser3_token = newUser3['token']
    
    # create a channel (inputerror)
    with pytest.raises(InputError):
        channels_create(newUser3_token, 'GeneralGeneralGeneral', True)
