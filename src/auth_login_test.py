import pytest

from auth import auth_login, auth_register, auth_logout 
from error import InputError
from email_test import check 

def test_login_correct():
    """
    Testing when the user logs in correctly (correct email syntax, correct password)
    """
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    user1_id = user_one['u_id']

    login_user = auth_login('student.test@unsw.edu.au','!@678hello')
    user2_id = login_user['u_id']

    # Checks the user has successfully logged into the correct account 
    # by confirming the register user ID is the same as the log-in user ID 

    assert user1_id == user2_id 


def test_login_no_email_domain():
    """
    Testing when user attempts to log in without entering their email domain.
    Email entered is not a valid email using the method provided in Project Specs.
    """     
    auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')

    with pytest.raises(InputError):
        auth_login('student.test@','!@678hello')    
        
        
def test_login_no_email_atsign():
    """
    Testing when user attempts to log in without entering @ within their email.
    Email entered is not a valid email using the method provided in Project Specs.
    """
    auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
    with pytest.raises(InputError):
        auth_login('student.testunsw.edu.au','!@678hello')


def test_login_user_exists():
    """
    Testing when user attempts to log in but their account does not exist.
    Email entered does not belong to a user.
    """
    
    auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test') 
    
    
    with pytest.raises(InputError):
        auth_login('user_doesnt_exist@unsw.edu.au','I_am_incorrect')
    

def test_login_incorrect_password():
    """
    Testing when user attempts to log in with the incorrect password
    """
    auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
    with pytest.raises(InputError):
        auth_login('student.test@unsw.edu.au','I_am_incorrect')
    
    
