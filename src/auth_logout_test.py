import pytest

from auth import auth_login, auth_register, auth_logout 

from error import InputError

   
def test_logout_correct():
    """
    A correct instance: A user correctly logs out of their account. 
    A valid token is given, the user successfully logs out & it returns true.
    """

    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    auth_login('student.test@unsw.edu.au','!@678hello')
    u_id1 = user_one['u_id']
    token1 = user_one['token']
    
    return1 = auth_logout(token1)
    assert return1['is_success'] == True

def test_logout_invalid_token():
    """
    An invalid token is given. The user is not able to log out.
    Is_Success returns false
    """
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    auth_login('student.test@unsw.edu.au','!@678hello')
    u_id1 = user_one['u_id']
    token1 = user_one['token']

    
    return1 = auth_logout('Invalid Token')
    assert return1['is_success'] == False

def test_logout_twice():
    """
    When a user tries to login and logout of their account twice
    A valid token is given, the user attempts to log out & it returns true.
    """

    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    auth_login('student.test@unsw.edu.au','!@678hello')
    u_id1 = user_one['u_id']
    token1 = user_one['token']
    
    return1 = auth_logout(token1)
    assert return1['is_success'] == True

    auth_login('student.test@unsw.edu.au','!@678hello')
    return2 = auth_logout(token1)
    assert return2['is_success'] == True