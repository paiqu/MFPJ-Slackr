'''Route implement for auth/passwordreset/reset'''
from json import dumps
from flask import Blueprint, request
from error import InputError
from data import getData

PASSWORDRESET_RESET = Blueprint('passwordreset_reset', __name__)

@PASSWORDRESET_RESET.route('/auth/passwordreset/reset', methods=['POST'])
def reset_password():
    '''function for route passwordreset_reset'''
    info = request.get_json()
    reset_code = str(info['reset_code'])
    new_password = str(info['new_password'])
    return dumps(passwordreset_reset(reset_code, new_password))

def passwordreset_reset(reset_code, new_password):
    '''route for passwordreset/reset'''
    if len(new_password) < 6:
        raise InputError("This password is too short. Must be at least 6 characters")

    valid_code = 'no'
    data = getData()
    for user in data['users']:
        if user['reset_code'] == reset_code:
            user['password'] = new_password
            user['reset_code'] = ''
            valid_code = 'yes'

    if valid_code == 'no':
        raise InputError("Not a valid reset code")

    return {}
