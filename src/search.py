'''Route implementation for search'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid
from data import getData

SEARCH = Blueprint('search', __name__)

@SEARCH.route('/search', methods=['GET'])

def request_get():
    '''function for route user/profile'''
    token = request.args.get('token')
    query_str = request.args.get('query_str')
    return dumps(search(token, query_str))

def search(token, query_str):
    '''
    Given a query string, return a collection of messages in all of the channels
    that the user has joined that match the query. Results are sorted from most recent
    message to least recent message.
    '''

    DATA = getData()
    messages = DATA['messages']
    reacts = DATA['reacts']

    messagelist = {'messages':[]}
    for message in messages:
        #find the target message and add information
        if str(query_str) in message['message_content']:
            message_info = {}
            message_info['message_id'] = message['message_id']
            message_info['u_id'] = message['sender_id']
            message_info['message'] = message['message_content']
            message_info['time_created'] = message['time_created']
            # create a react list of ths message
            react_collect = []
            for react in reacts:
                # find the reacts of this message
                if react['message_id'] == message['message_id']:
                    #if react is empty or it has not had this react, append a new react
                    #if react has already been in this list, just append the user_id
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
            #check whether the given user reacts
            for i in react_collect:
                for user_id in i['u_ids']:
                    if token_to_uid(token) == user_id:
                        i['is_this_user_reacted'] = True

            message_info['reacts'] = react_collect
            message_info['is_pinned'] = message['is_pin']
            messagelist['messages'].append(message_info)
    # reverse the list
    messagelist['messages'].reverse()
    return messagelist
