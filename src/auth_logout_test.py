from auth import auth_login, auth_register, auth_logout 
import pytest
from error import InputError

   
def test_logout_correct():
    """
    An correct instance: A user correctly logs out of their account 
    """
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
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    login_user = auth_login('student.test@unsw.edu.au','!@678hello')
    u_id1 = login_user['u_id']
    token1 = login_user['token']
    
    auth_logout(login_user['token'])
    auth_logout(login_user['token'])
    assert login_user['token'] == False