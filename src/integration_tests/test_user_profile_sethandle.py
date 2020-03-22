import pytest
from user import user_profile, user_profile_sethandle
from auth import auth_register 
from error import InputError

"""
Test the normal case: 
One user set the handle_str
Two user set the handle_str

InputError:
The first case:handle string entered between 3 and 20 character
The second case: handle string entered is already used
"""
    #This function will test the normal case that one user set the handle name 
def test_user_handle_success_one():
    
    #create the user
    user_zero = auth_register('z4357621@unde.edu.au', 'T64782', 'Tim', 'Puilet')
    user_id_zero = user_zero['u_id']
    token_zero = user_zero['token']
    
    #set the new handle string
    user_profile_sethandle(token_zero,'Hemil')
    
    #check whether the handle can be setted
    user_dict = user_profile(token_zero, user_id_zero)
    
    assert user_dict['user']['handle_str'] == 'Hem'
    
    #This function will test the success case that two user set the handle name
def test_user_handle_success_two():
    #create the user
    user_one = auth_register('z9327481@unsw.edu.au', 'Geily7481', 'Grey', 'Eily')
    user_id_one = user_one['u_id']
    token_one = user_one['token']
    
    #create the another user
    user_two = auth_register('z8466789@unsw.edu.au', 'TimdsmLiew', 'Dnne', 'Lmi')
    user_id_two = user_two["u_id"]
    token_two = user_two["token"]
    
    #set the new handle string for first user
    user_profile_sethandle(token_one,'Grhy')
    
    #set the new handle string for second user
    user_profile_sethandle(token_two,'Dlle')
    
    #check whether the handle can be setted for first user
    user_dict = user_profile(token_one, user_id_one)
    
    #check whether the handle can be setted for second user
    user_dict_two = user_profile(token_two, user_id_two)
    
    assert user_dict['user']['handle_str'] == 'Grhy'
    assert user_dict_two['user']['handle_str'] == 'Dlle'
       
    #This function is to test when the handle out of 20 character
def test_user_handle_inputError_one():
    
    #create the user
    user_one = auth_register('z2137682@unsw.edu.au', 'TimmLiew', 'Timm', 'Li')
    user_id_one = user_one['u_id']
    token_one = user_one['token']
    
    #if the user entered out of 20 character->InputError
    with pytest.raises(InputError):
        user_profile_sethandle(token_one,'a' * 1000)
    
    #This function will test when the handle between 0 and 2
def test_user_handle_inputError_two():
    
    #create the user
    user_one = auth_register('z6925391@unsw.edu.au', 'Fly5391', 'Tinne', 'Lily')
    user_id_one = user_one['u_id']
    token_one = user_one['token']
        
    #if the user entered between 0 and 2->InputError
    with pytest.raises(InputError):
        user_profile_sethandle(token_one,'a' * 2)    


    #This function is to test the second case
def test_user_handle_inputError_three():
    
    #create the user
    user_two = auth_register('z6677442@unsw.edu.au', 'TiLiw', 'Tmmaeno', 'Aaabc')
    user_id_two = user_two['u_id']
    token_two = user_two['token']
    
    #create the another user
    user_three = auth_register('z5327481@unsw.edu.au', 'TimdsmLiew', 'Dandmm', 'Lmi')
    user_id_three = user_three['u_id']
    token_three = user_three['token']
    
    #set the handle for the first user
    user_profile_sethandle(token_two,'TimAaab')
    
    #if handle string is already existed->InputError
    with pytest.raises(InputError):
        user_profile_sethandle(token_three,'TimAaab')
    
    
