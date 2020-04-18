'''Route implementation for auth/login'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid, user_exists_check
from error import InputError, AccessError
from token_functions import generate_token
from valid_email import check 

from data import DATA, getData


LOGIN = Blueprint('login', __name__)



def sendSuccess(DATA):
    return dumps(DATA)

def sendError(message):
    return dumps({
        '_error' : message,
    })

def getUserFromToken(token):
    global SECRET
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

    if check(email) == False:
        raise InputError("This is not a valid email")

    if user_exists_check(email) == False:
        raise InputError("Email entered does not belong to a user")
       
    for user in data['users']:
        if user['email'] == email:
                if user['email'] == email and user['password'] == password:
                    user['is_login'] = True
                    user['login'] = generate_token()
                    return dumps({
                        'u_id': user['u_id'],
                        'token' : user['login']   
                    })
                else: 
                    raise InputError("Password incorrect")
        
            
        
            
    

    

