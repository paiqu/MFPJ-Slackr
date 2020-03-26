'''Route implementation for auth/logout'''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError
from token_functions import generateToken
from auth_login import login, auth_login

from data import DATA, getData

def sendSuccess(DATA):
    return dumps(DATA)

def sendError(message):
    return dumps({
        '_error' : message,
    })

LOGOUT = Blueprint('logout', __name__)

@LOGOUT.route('/auth/logout', methods=['POST'])
def logout(token):
    token = request.form.get('token')
    

def auth_logout(token):
    data = getData()
    for user in data['users']:
        if user['email'] == email and user['password'] == hashPassword(password):
            return sendSuccess({
                'token': generateToken(email),
            })
    return sendError('Email or password incorrect') 
