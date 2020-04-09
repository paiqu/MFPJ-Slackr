'''Route implementation for auth/login'''
from json import dumps
from flask import Blueprint, request
import jwt
from check_functions import user_exists_check
from error import InputError
from valid_email import check
from data import getData, SECRET


LOGIN = Blueprint('login', __name__)



def sendSuccess(DATA):
    '''
    Functions that returns info if success
    '''
    return dumps(DATA)

def sendError(message):
    '''
    Returns error if there is an error in returning info for a function
    '''
    return dumps({
        '_error' : message,
    })

def getUserFromToken(token):
    '''
    Returns a user email from the supplied token
    '''

    decoded = jwt.decode(token, SECRET, algorithms=['HS256'])
    return decoded['email']
    
'''
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()
'''

@LOGIN.route('/auth/login', methods=['POST'])
def login():
    '''
    This function collects the information/parameters and calls the auth_login function
    '''
    info = request.get_json()

    email = info['email']
    password = info['password']

    # must return { u_id, token }
    return auth_login(email, password)



def auth_login(email, password):
    '''
    This function authenticates the token to show the user is logged in
    changes is_login to false
    '''
    data = getData()

    if not check(email):
        raise InputError("This is not a valid email")

    if not user_exists_check(email):
        raise InputError("Email entered does not belong to a user")

    for user in data['users']:
        if user['email'] == email:
            if user['email'] == email and user['password'] == password:
                user['is_login'] = True
                return dumps({
                    'u_id': user['u_id'],
                    'token' : user['token']
                })

            raise InputError("Email or password incorrect")
