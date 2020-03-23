
DATA = {
    'users': [], # a list of users {u_id: user_1}
    'channels': [] # a list of channels  {channel_id: channel_1}
}

SECRET = 'MFPJ'

def getData():
    global DATA
    return DATA

def getSecret():
    global SECRET
    return SECRET