from auth import auth_login 
from auth import auth_register 
import pytest
from error import InputError


def test_register():



def test_login1():
    assert login == 'token'
    



def test_echo():
    assert echo.echo("1") == "1", "1 == 1"
    assert echo.echo("abc") == "abc", "abc == abc"
    assert echo.echo("trump") == "trump", "trump == trump"

def test_echo_except():
    with pytest.raises(InputError) as e:
        assert echo.echo("echo")
