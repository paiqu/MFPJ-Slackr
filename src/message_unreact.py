from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, message_id_check
from error import InputError
from data import DATA, getData

UNREACT = Blueprint('message_react', __name__)

@REACT.route('/message/unreact', method=[POST])
def react():
    info = request.get_json()
    token = info['token']
    message_id = int(info['message_id'])
    react_id = int(info['react_id'])
    
    return dumps(message_unreact(token, message_id, react_id))
    
def message_unreact(token, message_id, react_id):
    global DATA
    messages = DATA['messages']
    reacts = DATA['reacts']
    
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
    if exist == 0:
        raise InputError("Not existing the react_id")
            
    for i in reacts:
        if i['message_id'] == message_id and i['react_id'] == react_id and i['u_id'] == token_to_uid(token):
           reacts.remove()
           
           
    return {}
                        
