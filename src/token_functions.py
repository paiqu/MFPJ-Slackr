'''This file stores token functions'''
import jwt
from data import get_Secret, LOGIN_COUNT

login_count = 0

def generate_register_token(u_id):
    '''
    convert a u_id to token. Encode it with HS256
    This is for register token
    '''
    SECRET = get_Secret()

    encoded = jwt.encode({'u_id': str(u_id)}, SECRET, algorithm="HS256")

    return str(encoded)


def generate_token():
    '''
    convert a u_id to token. Encode it with HS256
    This is for login tokens
    '''
    global LOGIN_COUNT
    LOGIN_COUNT += 1
    SECRET = get_Secret()

    encoded = jwt.encode({'count': str(login_count)}, SECRET, algorithm="HS256")

    return str(encoded)

if __name__ == "__main__":
    print(generate_register_token(1))
    