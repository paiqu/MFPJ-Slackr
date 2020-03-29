'''This file stores token functions'''
import jwt
from data import DATA, get_Secret

def generate_token(u_id):
    ''' convert a u_id to token. Encode it with HS256 '''
    SECRET = get_Secret()

    encoded = jwt.encode({'u_id': str(u_id)}, SECRET, algorithm="HS256")

    return str(encoded)

if __name__ == "__main__":
    print(generate_token(2345))