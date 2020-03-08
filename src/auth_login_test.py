import pytest

from auth import auth_login, auth_register, auth_logout 
from error import InputError

def test_login_correct():
    """
    Testing when the user logs in correctly (correct email syntax, correct password)
    """
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    login_user = auth_login('student.test@unsw.edu.au','!@678hello')
### Using assert - check the user ID and token are the same 
###Register token and log in token are the same 



def test_login_no_email_domain():
    """
    Testing when user attempts to log in without entering their email domain.
    Email entered is not a valid email using the method provided in Project Specs.
    """     
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')

    with pytest.raises(InputError) as e:
        login_user = auth_login('student.test@','!@678hello')    
        
        
def test_login_no_email_atsign():
    """
    Testing when user attempts to log in without entering @ within their email.
    Email entered is not a valid email using the method provided in Project Specs.
    """
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
    with pytest.raises(InputError) as e:
        login_user = auth_login('student.testunsw.edu.au','!@678hello')


def test_login_user_exists():
    """
    Testing when user attempts to log in but their account does not exist.
    Email entered does not belong to a user.
    """
    ### FIX THIS
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test') 
    u_id1 = user_one['u_id']
    token1 = user_one['token']
    
    
    with pytest.raises(InputError) as e:
        auth_login('user_doesnt_exist@unsw.edu.au','I_am_incorrect')
    '''
    assert u_id1 != u_id2
    login_user = auth_login('student.test@unsw.edu.au','!@678hello')
    u_id2 = login_user['u_id']
    token2= login_user['token']
    '''

def test_login_incorrect_password():
    """
    Testing when user attempts to log in with the incorrect password
    """
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
    with pytest.raises(InputError) as e:
        auth_login('student.test@unsw.edu.au','I_am_incorrect')
    
    
