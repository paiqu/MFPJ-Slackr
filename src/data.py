from class_file import User, Channel, Message, React, Standup
import os
import pickle
DATA = {
    'users': [], # a list of users {u_id: user_1}
    'channels': [], # a list of channels  {channel_id: channel_1}
    'messages': [], # a list of messages
    'reacts': [], # a list of reacts
    'standups': [], # a list of standups
    'users_count': 0,
    'channels_count': 0,
    'messages_count': 0
}

if os.path.exists('dataStore.p'):
    DATA = pickle.load(open('dataStore.p', 'rb'))


SECRET = 'MFPJ'

def getData():
    global DATA
    return DATA

def get_Secret():
    global SECRET
    return SECRET


