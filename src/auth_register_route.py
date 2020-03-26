'''Route implementation for auth/register'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError
from token_functions import generate_token

from data import DATA, getData


REGISTER = Blueprint('register', __name__)


def sendSuccess(DATA):
    return dumps(DATA)

def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generateHandle(firstName, lastName):
    handle = firstName + lastName 
    return handle

#def generateUserID():


@REGISTER.route('/auth/register', methods=['POST'])

def register():
    '''function for route auth/register'''

    info = request.get_json()
    
    email = info['email']
    password = info['password']
    firstName = info['First Name']
    lastName = info['Last Name']

    auth_register(email, password, firstName, lastName)


    #Need to return { u_id, token }
    return dumps({})

def auth_register(email, password, firstName, lastName):
    data = getData()
    handle = generateHandle(firstName, lastName)
    u_id = generateUserID(email)
    data['users'].append({
        'email': email,
        'password': hashPassword(password),
        'First Name': firstName,
        'Last Name': lastName,
        'Handle': handle,
        'U_ID': u_id,
    })
    
    print(data)
    return sendSuccess({
        'token': generate_token(email),
    })

