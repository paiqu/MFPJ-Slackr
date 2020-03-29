from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid
from error import InputError, AccessError

from class_file import User
from data import *

ALL = Blueprint('user_all', __name__)

@ALL.route('/user/all', methods=['GET'])
def all():
    '''function for route of users all'''
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    return dumps(user_all(token, u_id))
   

def user_all(token, u_id):
    '''
    Given a token, list all users associated with information 
    
    '''

    DATA = getData()
    users = DATA['users']

    users.append(vars(User(u_id = 23, email = 'z54634652@unsw.edu.au', name_first = 'Matiea', name_last = 'Ben', handle = '')))
    
    user = {'user':{}}
      
    return users