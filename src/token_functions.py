'''This file stores token functions'''
import jwt

def generate_token(u_id):
    ''' convert a u_id to token. Encode it with HS256 '''
    global SECRET
    encoded = jwt.encode({'u_id': str(u_id)}, SECRET, algorithm="HS256")
    return str(encoded)
