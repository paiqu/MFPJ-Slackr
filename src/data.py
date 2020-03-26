from class_file import User, Channel, Message, Time, React

DATA = {
    'users': [], # a list of users {u_id: user_1}
    'channels': [], # a list of channels  {channel_id: channel_1}
    'messages': [], # a list of messages
    'times': [], # a list of time
    'reacts':[] # a list of reacts
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
