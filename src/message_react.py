'''Route implementation for message/react'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, message_id_check
from error import InputError
from class_file import React
from data import DATA

MESSAGE_REACT = Blueprint('message_react', __name__)

@MESSAGE_REACT.route('/message/react', methods=['POST'])
def react():
    '''function for route message/react'''
    info = request.get_json()
    token = info['token']
    message_id = int(info['message_id'])
    react_id = int(info['react_id'])
    return dumps(message_react(token, message_id, react_id))

def message_react(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of,
    add a "react" to that particular message
    '''
    global DATA
    reacts = DATA['reacts']

    if not message_id_check(message_id):
        raise InputError("Message ID is not valid")
    if react_id != 1:
        raise InputError("React ID is not valid")

    # check the react_id exist or not
    exist = False
    for i in reacts:
        if i['message_id'] == message_id:
            if i['u_id'] == token_to_uid(token):
                if i['react_id'] == react_id:
                    exist = True
    if exist == True:
        raise InputError("Already existing the react_id")
    reacts.append(vars(React(message_id, token_to_uid(token), react_id)))

    return {}
