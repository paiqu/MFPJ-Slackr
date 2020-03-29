from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid
from error import InputError, AccessError

from class_file import User
from data import *

ALL = Blueprint('users_all', __name__)

@ALL.route('/users/all', methods=['GET'])
def all():
    '''function for route of users all'''
    token = request.args.get('token')
    u_id = request.args.get('u_id')
    return dumps(users_all(token, u_id))
   

def users_all(token, u_id):
    '''
    Given a token, list all users associated with information 
    
    '''

    DATA = getData()
    users = DATA['users']
      
    return users