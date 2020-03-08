import pytest

from auth import auth_login, auth_register, auth_logout 

from error import InputError

   
def test_logout_correct():
    """
    A correct instance: A user correctly logs out of their account. 
    A valid token is given, the user successfully logs out & it returns true.
    """

    #### This function retrns is_success - not token 
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    login_user = auth_login('student.test@unsw.edu.au','!@678hello')
    u_id1 = login_user['u_id']
    token1 = login_user['token']
    
    auth_logout(login_user['token'])
    assert login_user['token'] == True

def test_logout_twice():
    """
    When a user tries to logout of their account twice
    """

     #### This function retrns is_success - not token 
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    login_user = auth_login('student.test@unsw.edu.au','!@678hello')
    u_id1 = login_user['u_id']
    token1 = login_user['token']
    
    auth_logout(login_user['token'])
    auth_logout(login_user['token'])
    assert login_user['token'] == False