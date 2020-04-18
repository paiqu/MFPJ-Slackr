'''file to store data'''

DATA = {
    'users': [], # a list of users
    'channels': [], # a list of channels
    'messages': [], # a list of messages
    'reacts': [], # a list of reacts
    'standups': [], # a list of standups
    'users_count': 0,
    'channels_count': 0,
    'messages_count': 0
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

HANGMAN_WORD = ""
BOT_TOKEN = ""
CORRECT_GUESSED = []
WRONG_GUESS = []
CORRECT_TIMES = 0
WRONG_TIMES = 0
GUESSED = ''
HAVE_GUESSED = []
