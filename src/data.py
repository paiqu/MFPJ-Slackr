from class_file import User, Channel, Message, React, Standup

DATA = {
    'users': [], # a list of users {u_id: user_1}
    'channels': [], # a list of channels  {channel_id: channel_1}
    'messages': [], # a list of messages
    'reacts': [], # a list of reacts
    'standups': [], # a list of standups
}

SECRET = 'MFPJ'


def getData():
    global DATA
    return DATA

def get_Secret():
    global SECRET
    return SECRET

CHANNELS_COUNT = 0
MESSAGE_COUNT = 0
