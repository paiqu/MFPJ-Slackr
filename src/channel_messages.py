'''route implement for channel/messages '''
from json import dumps
from flask import Blueprint, request
from check_functions import channel_id_check, channel_member_check, token_to_uid
from error import InputError, AccessError
from class_file import User, Message, Channel, React
from data import DATA, getData

CHANNEL_MESSAGES = Blueprint('channel_messages', __name__)

@CHANNEL_MESSAGES.route('/channel/messages', methods=['GET'])
def route_channel_messages():
    # function for route channel/messages
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    
    return dumps(channel_messages(token, channel_id, start))

def channel_messages(token, channel_id, start):
    '''
    Given a token, channel_id and start, 
    if there is more than 50 messages in channels after 'start'-a index,
    return 50 messages in that channel and 'start' + 50 as the 'end'
    otherwise return all messages and '-1' as the 'end'
    '''
    DATA = getData()
    users = DATA['users']
    channels = DATA['channels']
    messages = DATA['messages']
    reacts = DATA['reacts']
    '''
    users.append(vars(User(u_id=1, email='123@55.com', name_first='mike', name_last='cop')))
    channels.append(vars(Channel(channel_id = 1, channel_name = 'name')))
    channels[0]['members'].append(users[0])
    channels[0]['owners'].append(users[0])
    messages.append(vars(Message(message_content = 'first', message_id = 1, channel_id = 1, sender_id = 1, time = 1231)))
    messages.append(vars(Message(message_content = 'second', message_id = 2, channel_id = 1, sender_id = 1, time = 1231)))
    messages.append(vars(Message(message_content = 'third', message_id = 3, channel_id = 1, sender_id = 1, time = 1231)))
    '''
    
    if not channel_id_check(channel_id):
        raise InputError("Invalid channel_id")
        
    if not channel_member_check(channel_id, token):
        raise AccessError("Authorised user is not a member of channel with channel_id")


    # create a list which contains only the selected channel's messages_list
    messages_list = []
    for i in messages:
        if i['channel_id'] == channel_id:
            message_info = {}
            message_info['message_id'] = i['message_id']
            message_info['u_id'] = i['sender_id']
            message_info['message'] = i['message_content']
            message_info['time_created'] = i['time_created']
            react_collect = []
            for react in reacts:
                # find the reacts of this message
                if react['message_id'] == i['message_id']:
                    ''' 
                    if react is empty or it has not had this react, append a new react 
                    if react has already been in this list, just append the user_id
                    '''
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
            for j in react_collect:
                for user_id in j['u_ids']:
                    if token_to_uid(token) == user_id:
                        j['is_this_user_reacted'] = True
          
            message_info['reacts'] = react_collect
            message_info['is_pinned'] = i['is_pin']
            messages_list.append(message_info)

    if start >= len(messages_list) and len(messages_list) != 0:
        raise InputError("Invalid start")
        
    # formate output {messages, start, end}
    out_dict = {}
    messages_list.reverse()
    new_list = messages_list[start:]
    
    if 50 > len(new_list):
        out_dict['messages'] = new_list
        out_dict['start'] = start
        out_dict['end'] = -1
    else: 
        out_dict['messages'] = new_list[0:50]
        out_dict['start'] = start
        out_dict['end'] = start + 50
          
    return out_dict

