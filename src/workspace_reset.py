'''route implementation for workspace/reset'''
from json import dumps
from flask import Blueprint
from data import *



RESET = Blueprint('workspace_reset', __name__)

@RESET.route('/workspace/reset', methods=['POST'])
def reset():
    '''reset workspace'''
    global DATA
    DATA['users'].clear()
    DATA['channels'].clear()
    DATA['messages'].clear()
    DATA['reacts'].clear()
    DATA['standups'].clear()
    DATA['users_count'] = 0
    DATA['channels_count'] = 0
    DATA['messages_count'] = 0


    global HANGMAN_WORD
    global BOT_TOKEN
    global CORRECT_GUESSED
    global WRONG_GUESS
    global CORRECT_TIMES
    global WRONG_TIMES
    global GUESSED
    global HAVE_GUESSED

    HANGMAN_WORD = ""
    BOT_TOKEN = ""
    CORRECT_GUESSED.clear()
    WRONG_GUESS.clear()
    CORRECT_TIMES = 0
    WRONG_TIMES = 0
    GUESSED = ''
    HAVE_GUESSED.clear()




    return dumps({})
