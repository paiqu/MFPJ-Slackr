'''Route implementation for auth/login'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError
from token_functions import generateToken

from data import DATA, getData


LOGIN = Blueprint('login', __name__)

valid_token = False

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

def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()


@LOGIN.route('/auth/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    return auth_login(email, password)
    


def auth_login(email, password):
    data = getData()
    global valid_token
    for user in data['users']:
        ####CHANGE USERNAME TO EMAIL 
        if user['email'] == email and user['password'] == hashPassword(password):
            valid_token = True
            return sendSuccess({
                'token': generateToken(email),
            })
    valid_token = False
    return sendError('Email or password incorrect') 
    

