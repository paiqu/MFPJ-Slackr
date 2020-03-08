import pytest

from auth import auth_login, auth_register, auth_logout

from user import user_profile

from error import InputError

def test_register_correct():
    """
    This test function is when a user is registered correctly.
    It should not fail any tests.
    """
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    user1_id = user_one['u_id']
    user1_token = user_one['token']
    user1_profile = user_profile(user1_token, user1_id)

    # Testing that user_1 has been correctly registered by checking the handle 
    assert user1_profile['handle'] =='studenttest'


def test_register_invalid_email():
    """
    Testing when an email is invalid: does not contain @ symbol
    """
    with pytest.raises(InputError):
        auth_register('student.testunsw.edu.au','!@678hello', 'Student', 'Test') 

def test_register_invalid_email_two():
    """
    Testing when an email is invalid: does not have a domain
    """
    with pytest.raises(InputError):
        auth_register('student.test@','!@678hello', 'Student', 'Test') 
        

def test_register_twice():
    """
    Testing when the user registers twice (with same email, password, F-Name, L-Name)
    Email address is already being used by another user.
    """
    
    auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')

    with pytest.raises(InputError):
        auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')   
    
def test_register_short_password():
    '''
    Testing too short password, should raise an error
    Password entered is less than 6 characters long
    '''

    short_password = 'too_short'
    with pytest.raises(InputError):
        auth_register('student.test@unsw.edu.au',short_password, 'Student', 'Test')
        
def test_register_short_fname():
    """
    Testing when registering with a first name < 1 character
    """

    short_fname = ''
    with pytest.raises(InputError):
        auth_register('student.test@unsw.edu.au','!@678hello', short_fname, 'Test')
    
def test_register_long_fname():
    """
    Testing when registering with a first name > 50 characters
    """

    long_fname = '***Thisfirstnameistoolonganditshouldreturninvalid***'

    with pytest.raises(InputError):
        auth_register('student.test@unsw.edu.au','!@678hello', long_fname , 'Test')
        
def test_register_short_lname():
    """
    Testing when registering with a last name < 1 character
    """

    short_lname = ''

    with pytest.raises(InputError):
        auth_register('student.test@unsw.edu.au','!@678hello', 'Student', short_lname)

def test_register_long_lname():
    """
    Testing when registering with a last name > 50 characters
    """

    long_lname = '***Thislastnameistoolonganditshouldreturninvalid***'
    
    with pytest.raises(InputError):
        auth_register('student.test@unsw.edu.au','!@678hello', 'Student', long_lname)

