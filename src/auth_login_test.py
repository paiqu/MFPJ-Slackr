from auth import auth_login, auth_register, auth_logout 
import pytest
from error import InputError

#Tests for the function auth_register 
def test_register_correct():
    user_one = register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
def test_register_short_password():
    with pytest.raises(InputError) as e:
        register('student.test@unsw.edu.au','678', 'Student', 'Test')
        
def test_register_invalid_email():
    with pytest.raises(InputError) as e:
        register('student.testunsw.edu.au','!@678hello', 'Student', 'Test')
        
def test_register_invalid_fname():
    with pytest.raises(InputError) as e:
        register('student.test@unsw.edu.au','!@678hello', '', 'Test')
        
def test_register_invalid_lname():
    with pytest.raises(InputError) as e:
        register('student.test@unsw.edu.au','!@678hello', 'Student', '')
        
def test_register_twice():
    user_one = register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')

    with pytest.raises(InputError) as e:
        user_two = register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
#Tests for the function auth_login     
#check that the user has registered an account 
def test_login_correct():
    user_one = register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    login_user = login('student.test@unsw.edu.au','!@678hello')

def test_login_user_exists():
    user_one = register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test') 
    u_id1 = user_one['u_id']
    token1 = user_one['token']
    
    
    login_user = login('student.test@unsw.edu.au','!@678hello')
    u_id2 = login_user['u_id']
    token2= login_user['token']
    
    assert u_id1 == u_id2
    
def test_login_incorrect_password():
    user_one = register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
    login_user = login('student.test@unsw.edu.au','!@678hello')
    
    assert user_one['password'] == login_user['password']
    
    
def test_login_no_email_domain():
     with pytest.raises(InputError) as e:
        login_user = login('student.test@','!@678hello')
        
        
        
def test_login_no_email_atsign():
    user_one = register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    
    with pytest.raises(InputError) as e:
        login_user = login('student.testunsw.edu.au','!@678hello', 'Student', 'Test')
    
def test_logout_correct():
    user_one = register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    login_user = login('student.test@unsw.edu.au','!@678hello')
    u_id1 = login_user['u_id']
    token1 = login_user['token']
    
    logout(login_user['token'])
    assert login_user['token'] == True

def test_logout_twice():
    user_one = register('student.test@unsw.edu.au','!@678hello', 'Student', 'Test')
    login_user = login('student.test@unsw.edu.au','!@678hello')
    u_id1 = login_user['u_id']
    token1 = login_user['token']
    
    logout(login_user['token'])
    logout(login_user['token'])
    assert login_user['token'] == False
    
    
"""
def test_echo():
    assert echo.echo("1") == "1", "1 == 1"
    assert echo.echo("abc") == "abc", "abc == abc"
    assert echo.echo("trump") == "trump", "trump == trump"

def test_echo_except():
    with pytest.raises(InputError) as e:
        assert echo.echo("echo")
"""
