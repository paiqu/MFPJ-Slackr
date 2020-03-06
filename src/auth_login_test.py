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
    with pytest.raises(InputError) as e:
        auth_register('student.testunsw.edu.au','!@678hello', 'Student', 'Test')
        
def test_register_invalid_fname():
    with pytest.raises(InputError) as e:
        auth_register('student.test@unsw.edu.au','!@678hello', '', 'Test')
        
def test_register_invalid_lname():
    with pytest.raises(InputError) as e:
        auth_register('student.test@unsw.edu.au','!@678hello', 'Student', '')
        
def test_register_twice():
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')

    with pytest.raises(InputError) as e:
        user_two = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
#Tests for the function auth_login     
#check that the user has registered an account 
def test_login_correct():
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    login_user = auth_login('student.test@unsw.edu.au','!@678hello')

def test_login_user_exists():
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test') 
    u_id1 = user_one['u_id']
    token1 = user_one['token']
    
    
    login_user = auth_login('student.test@unsw.edu.au','!@678hello')
    u_id2 = login_user['u_id']
    token2= login_user['token']
    
    assert u_id1 == u_id2
    
def test_login_incorrect_password():
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
    login_user = auth_login('student.test@unsw.edu.au','hello')
    
    assert user_one['password'] != login_user['password']
    
    
def test_login_no_email_domain():
     with pytest.raises(InputError) as e:
        login_user = login('student.test@','!@678hello')
        
        
        
def test_login_no_email_atsign():
    user_one = auth_register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
    with pytest.raises(InputError) as e:
        login_user = auth_login('student.testunsw.edu.au','!@678hello', 'Student', 'Test')