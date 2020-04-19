'''file to store data'''
import os
import pickle
from class_file import User, Channel, Message, React, Standup

DATA = {
    'users': [], # a list of users
    'channels': [], # a list of channels
    'messages': [], # a list of messages
    'reacts': [], # a list of reacts
    'standups': [], # a list of standups
    'users_count': 0,
    'channels_count': 0,
    'messages_count': 0,
    'login_count': 0
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


HANGMAN_WORD = ""
BOT_TOKEN = ""
CORRECT_GUESSED = []
WRONG_GUESS = []
CORRECT_TIMES = 0
WRONG_TIMES = 0
GUESSED = ''
HAVE_GUESSED = []
