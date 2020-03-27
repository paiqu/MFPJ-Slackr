'''Route implementation for search'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid
from data import DATA, getData
from class_file import User, React, Message, Channel

SEARCH = Blueprint('search', __name__)

@SEARCH.route('/search', methods=['GET'])

def request_get():
    '''function for route user/profile'''
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(search(token,query_str))

def search(token, query_str):
    '''
    Given a query string, return a collection of messages in all of the channels 
    that the user has joined that match the query. Results are sorted from most recent 
    message to least recent message.
    '''
    
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    messages = DATA['messages']
    reacts = DATA['reacts']
    
    messagelist = {'messages':[]}
    users.append(vars(User(u_id=123, email='123@55.com', name_first='pai', name_last='qu', handle='')))   
    channels.append(vars(Channel(1,"Public")))
    channels[0]['members'].append(users[0])
    channels[0]['owners'].append(users[0])
    messages.append(vars(Message("hello",1,1,123,574820)))
    reacts.append(vars(React(1,123,1)))

    for message in messages:
        if str(query_str) in message['message_content']:
            message_info = {}
            message_info['message_id'] = message['message_id']
            message_info['u_id'] = message['sender_id']
            message_info['message'] = message['message_content']
            message_info['time_created'] = message['time_created']
            
            react_collect = []
            for react in reacts:
                
                if react['message_id'] == message['message_id']:
                    
                    if react_collect == []:
                        react_collect.append({'react_id': react['react_id'], 'u_ids': [react['u_id']], 'is_this_user_reacted': False})

                    else:   
                        for react_single in react_collect:
                        
                            is_react_in = False
                            if react_single['react_id'] == react['react_id']:
                                react_collect['react_single']['u_ids'].append(react['u_id'])
                                is_react_in = True
                        
                            if is_react_in == False:
                                react_collect.append({'react_id': react['react_id'], 'u_ids': [react['u_id']], 'is_this_user_reacted': False})
               
            for i in react_collect:
                for user in i['u_ids']:
                    if token_to_uid(token) == user:
                        i['is_this_user_reacted'] = True     

            message_info['reacts'] = react_collect 
                     
            message_info['is_pinned'] = message['is_pin']
    
            messagelist['messages'].append(message_info)
            
    return messagelist

