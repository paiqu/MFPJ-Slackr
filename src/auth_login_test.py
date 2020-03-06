from auth import auth_login, auth_register, auth_logout 
import pytest
from error import InputError

#Tests for the function auth_login     
#check that the user has registered an account 
def test_login_correct():
    """
    Testing when the user logs in correctly (correct email syntax, correct password)
    """
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    login_user = auth_login('student.test@unsw.edu.au','!@678hello')

def test_login_user_exists():
    """
    Testing when user attempts to log in but their account does not exist
    """
    ### FIX THIS
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test') 
    u_id1 = user_one['u_id']
    token1 = user_one['token']
    
    
    login_user = auth_login('student.test@unsw.edu.au','!@678hello')
    u_id2 = login_user['u_id']
    token2= login_user['token']
    
    assert u_id1 == u_id2
    
def test_login_incorrect_password():
    """
    Testing when user attempts to log in with the incorrect password
    """
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
    login_user = auth_login('student.test@unsw.edu.au','hello')
    
    assert user_one['password'] != login_user['password']
    
    
def test_login_no_email_domain():
    """
    Testing when user attempts to log in without entering their email domain
    """
     with pytest.raises(InputError) as e:
        login_user = login('student.test@','!@678hello')
        
        
        
def test_login_no_email_atsign():
    """
    Testing when user attempts to log in without entering @ within their email 
    """
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
    with pytest.raises(InputError) as e:
        login_user = auth_login('student.testunsw.edu.au','!@678hello', 'Student', 'Test')