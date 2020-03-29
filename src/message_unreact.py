'''Route implemetation for message/unreact'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid, message_id_check
from error import InputError
from class_file import User, Message, Channel, React
from data import DATA, getData

MESSAGE_UNREACT = Blueprint('message_unreact', __name__)

@MESSAGE_UNREACT.route('/message/unreact', methods=['POST'])
def react():
    '''function for route message/unreact'''
    info = request.get_json()
    token = info['token']
    message_id = int(info['message_id'])
    react_id = int(info['react_id'])
    
    return dumps(message_unreact(token, message_id, react_id))
    
def message_unreact(token, message_id, react_id):
    '''
    Given a message within a channel the authorised user is part of, 
    remove a "react" to that particular message
    '''
    global DATA
    messages = DATA['messages']
    users = DATA['users']
    channels = DATA['channels']
    reacts = DATA['reacts']
    '''
    users.append(vars(User(u_id=1, email='123@55.com', name_first='mike', name_last='cop', handle='')))
    channels.append(vars(Channel(channel_id = 1, channel_name = 'name')))
    channels[0]['members'].append(users[0])
    channels[0]['owners'].append(users[0])
    messages.append(vars(Message(message_content = 'first', message_id = 1, channel_id = 1, sender_id = 1, time = 1231)))
    reacts.append(vars(React(message_id = 1, u_id = 1, react_id = 1)))
    '''
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
    if exist == False:
        raise InputError("Not existing the react_id")
     
            
    for i in reacts:
        if i['message_id'] == message_id and i['react_id'] == react_id and i['u_id'] == token_to_uid(token):
           reacts.remove(i)
           
           
    return {}
                        
