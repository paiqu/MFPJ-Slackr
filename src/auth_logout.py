'''Route implementation for auth/logout'''
from json import dumps
from flask import Blueprint, request
from error import InputError

from data import getData

LOGOUT = Blueprint('logout', __name__)

@LOGOUT.route('/auth/logout', methods=['POST'])
def logout():
    '''
    This function collects the information/parameters and calls the auth_logout function
    '''
    info = request.get_json()

    token = info['token']

    # must return { is_success }
    return dumps(auth_logout(token))


def auth_logout(token):
    '''
    This function logs out with an authenticated token
    Changes is_login to false
    '''
    data = getData()
    for user in data['users']:
        if user['token'] == token:
            if user['is_login']:
                ###LOGS USER OUT - TOKEN BECOMES FALSE
                user['is_login'] = False
                new_dict = {}
                new_dict['is_success'] = True
                return new_dict

            raise InputError("Problem occurred while logging out")
