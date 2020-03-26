from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, message_id_check
from error import InputError
from data import DATA, getData

REACT = Blueprint('message_react', __name__)

@REACT.route('/message/react', method=[POST])
def react():
    info = request.get_json()
    token = info['token']
    message_id = int(info['message_id'])
    react_id = int(info['react_id'])
    
    return dumps(message_react(token, message_id, react_id))
    
def message_react(token, message_id, react_id):
    global DATA
    messages = DATA['messages']
    react = DATA['react']
    
    if not message_id_check(message_id):
        raise InputError("Message ID is not valid")
    if react_id != 1:
        raise InputError("React ID is not valid")
    
    exist = 0
    for i in reacts:
        if i['message_id'] == message_id:
            if i['react_id'] == react_id:
                if i['u_id'] == token_to_uid(token):
                    exist = 1
    if exist == 1:
        raise InputError("Already existing the react_id")
    
    vars(React(message_id, token_to_uid(token), react_id))
    
    return {}

