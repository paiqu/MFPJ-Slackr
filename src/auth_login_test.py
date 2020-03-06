import pytest

from auth import auth_login, auth_register, auth_logout 
from error import InputError, AccessError

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
    
    with pytest.raises(InputError) as e:
        auth_login('student.test@unsw.edu.au','I_am_incorrect')
    
    
def test_login_no_email_domain():
    """
    Testing when user attempts to log in without entering their email domain
    """     
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')

    with pytest.raises(InputError) as e:
        login_user = auth_login('student.test@','!@678hello')
        
        
        
def test_login_no_email_atsign():
    """
    Testing when user attempts to log in without entering @ within their email 
    """
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
    with pytest.raises(InputError) as e:
        login_user = auth_login('student.testunsw.edu.au','!@678hello')