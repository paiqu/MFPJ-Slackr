import pytest

from auth import auth_login, auth_register, auth_logout 

from error import InputError

def test_register_correct():
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')

    

    ##ADD THE ASSERT -- WE ARE NOT TESTING SOMETHING HERE 

def test_register_invalid_email():
    """
    Testing when an email is invalid: does not contain @ symbol
    """
    with pytest.raises(InputError) as e:
        auth_register('student.testunsw.edu.au','!@678hello', 'Student', 'Test') 

def test_register_twice():
    """
    Testing when the user registers twice (with same email, password, F-Name, L-Name)
    Email address is already being used by another user.
    """

    ###DON"T NEED TO ASSIGN A VARIABLE IF IM NOT GOING TO CALL IT AGAIN 
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')

    with pytest.raises(InputError) as e:
        user_two = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')   
    
def test_register_short_password():
    '''
    Testing too short password, should raise an error
    Password entered is less than 6 characters long
    '''
    with pytest.raises(InputError) as e:
        auth_register('student.test@unsw.edu.au','678', 'Student', 'Test')
        
def test_register_short_fname():
    """
    Testing when registering with a first name < 1 character
    """
    with pytest.raises(InputError) as e:
        auth_register('student.test@unsw.edu.au','!@678hello', '', 'Test')
    
def test_register_long_fname():
    """
    Testing when registering with a first name > 50 characters
    """

    ###ASSIGN LONG AND SHORT PASSWORDS TO A VARIABLE 
    with pytest.raises(InputError) as e:
        auth_register('student.test@unsw.edu.au','!@678hello', '***Thisfirstnameistoolonganditshouldreturninvalid***', 'Test')
        
def test_register_short_lname():
    """
    Testing when registering with a last name < 1 character
    """
    with pytest.raises(InputError) as e:
        auth_register('student.test@unsw.edu.au','!@678hello', 'Student', '')

def test_register_long_lname():
    """
    Testing when registering with a last name > 50 characters
    """
    with pytest.raises(InputError) as e:
        auth_register('student.test@unsw.edu.au','!@678hello', 'Student', '***Thislastnameistoolonganditshouldreturninvalid***')

    