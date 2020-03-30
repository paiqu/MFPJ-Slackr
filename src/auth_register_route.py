'''Route implementation for auth/register'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError
from token_functions import generate_token
from valid_email import check 
from class_file import User

from data import DATA, getData



REGISTER = Blueprint('register', __name__)


def sendSuccess(DATA):
    return dumps(DATA)

'''
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()
'''
def generateHandle(firstName, lastName):
    #add tests for generate handle 
    handle = firstName + lastName 
    return handle

# def generateUserID():
#     user_count = len(DATA['users'])
#     return user_count+1



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
    
    


    #This function will return { u_id, token }
    return auth_register(email, password, firstName, lastName)

def auth_register(email, password, name_first, name_last):
    '''
    This function creates a new user object and adds it to the user register list/dictionary 
    '''
    data = getData()
    
    if check(email) == False:
        raise InputError("This is not a valid email")

    for user in data['users']:
        if user['email'] == email:
            raise InputError("This email is already being used by another user")
    
    if len(password) < 6:
        raise InputError("This password is too short. Must be at least 6 characters")

    if (len(name_first) < 1) or (len(name_first) > 50):
        raise InputError("First Name must be between 1 and 50 characters")

    if (len(name_last) < 1) or (len(name_last) > 50):
        raise InputError("Last Name must be between 1 and 50 characters")

    data['users_count'] += 1
    generate_ID = data['users_count']
    user_1 = User(generate_ID, email, name_first, name_last)
    user_1.handle = generateHandle(name_first, name_last)
    user_1.token = str(generate_token(generate_ID))

    if data['users'] == []:
        user_1.is_slack_owner = True
        user_1.global_permission = 1
    

    user_1.password = password
    user_1 = vars(user_1)
    
    
    data['users'].append(user_1)
    
    return dumps({
        'u_id' : user_1['u_id'],
        'token': user_1['token']
    })
    

    

