import pytest

from auth import auth_login, auth_register, auth_logout 

from error import InputError

   
def test_logout_correct():
    """
    A correct instance: A user correctly logs out of their account. 
    A valid token is given, the user successfully logs out & it returns true.
    """

    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    login_user = auth_login('student.test@unsw.edu.au','!@678hello')
    u_id1 = login_user['u_id']
    token1 = login_user['token']
    
    auth_logout(login_user['token'])
    assert login_user['is_success'] == True

def test_logout_invalid_token():
    """
    An invalid token is given. The user is not able to log out.
    Is_Success returns false
    """
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    login_user = auth_login('student.test@unsw.edu.au','!@678hello')
    u_id1 = login_user['u_id']
    token1 = login_user['token']

    
    auth_logout('Invalid Token')
    assert login_user['is_success'] == False

def test_logout_twice():
    """
    When a user tries to logout of their account twice
    A invalid token is given, the user attempts to log out & it returns false.
    """

    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    login_user = auth_login('student.test@unsw.edu.au','!@678hello')
    u_id1 = login_user['u_id']
    token1 = login_user['token']
    
    auth_logout(login_user['token'])
    auth_logout(login_user['token'])
    assert login_user['is_success'] == False