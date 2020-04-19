'''This file stores token functions'''
import jwt
from data import get_Secret, getData

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
    DATA = getData()
    DATA['login_count'] += 1
    login_count = DATA['login_count']

    return int(login_count)


if __name__ == "__main__":
    print(generate_token())
    print(generate_token())

    print(generate_register_token(2))
