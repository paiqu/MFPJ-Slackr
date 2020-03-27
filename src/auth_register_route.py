'''Route implementation for auth/register'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError
from token_functions import generate_token
from valid_email import check 

from data import DATA, getData

user_count = 1

REGISTER = Blueprint('register', __name__)


def sendSuccess(DATA):
    return dumps(DATA)

def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generateHandle(firstName, lastName):

    #add tests for generate handle 
    handle = firstName + lastName 
    return handle

def generateUserID():
    global user_count 
    u_id = user_count 
    user_count += 1
    return u_id



@REGISTER.route('/auth/register', methods=['POST'])

def register():
    '''
    This function collects the information/parameters and calls the auth_register function
    '''

    info = request.get_json()
    
    
    email = info['email']
    password = info['password']
    firstName = info['name_first']
    lastName = info['name_last']
    
    
    auth_register(email, password, firstName, lastName)


    #Need to return { u_id, token }
    return dumps({})

def auth_register(email, password, name_first, name_last):
    
    data = getData()
    handle = ""
    return data
    
    generateHandle(firstName, lastName)
    u_id = generateUserID()

    #return u_id
    #####CREATE A USER CLASS 
    data['users'].append({
        'u_id': u_id,
        'email': email,
        'password': hashPassword(password),
        'name_first': firstName,
        'name_last': lastName,
        'handle': handle,
        
    })
    
    print(data)
    return sendSuccess({
        'token': generate_token(email),
        'u'
    })


    

