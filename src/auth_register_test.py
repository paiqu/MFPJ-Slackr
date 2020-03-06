from auth import auth_login, auth_register, auth_logout 
import pytest
from error import InputError


#Tests for the function auth_register 
def test_register_correct():
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
def test_register_short_password():
    '''
    Testing too short password, should raise an error
    '''
    with pytest.raises(InputError) as e:
        auth_register('student.test@unsw.edu.au','678', 'Student', 'Test')
        
def test_register_invalid_email():
    """
    Testing when an email is invalid: does not contain @ symbol
    """
    with pytest.raises(InputError) as e:
        auth_register('student.testunsw.edu.au','!@678hello', 'Student', 'Test')
        
def test_register_invalid_fname():
    """
    Testing when registering with a first name < 1 character
    """
    with pytest.raises(InputError) as e:
        auth_register('student.test@unsw.edu.au','!@678hello', '', 'Test')
        
def test_register_invalid_lname():
    """
    Testing when registering with a last name < 1 character
    """
    with pytest.raises(InputError) as e:
        auth_register('student.test@unsw.edu.au','!@678hello', 'Student', '')
        
def test_register_twice():
    """
    Testing when the user registers twice (with same email, password, F-Name, L-Name)
    """

    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')

    with pytest.raises(InputError) as e:
        user_two = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    