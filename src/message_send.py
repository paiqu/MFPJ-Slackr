'''Route implementation for message_send'''
import datetime
from json import dumps
import random
from flask import Blueprint, request
from check_functions import token_to_uid, channel_member_check, channel_game_on
from error import InputError, AccessError
from data import getData, HANGMAN_WORD, BOT_TOKEN, CORRECT_GUESSED, WRONG_GUESS, CORRECT_TIMES, WRONG_TIMES, GUESSED, HAVE_GUESSED
from class_file import Message, User
from phases import phases_list
from token_functions import generate_token


SENDMESSAGE = Blueprint('message_send', __name__)

@SENDMESSAGE.route('/message/send', methods=['POST'])
def request_get():
    '''request get for route message send'''
    info = request.get_json()
    token = info['token']
    channel_id = int(info['channel_id'])
    message = info['message']

    # If message starts with /hangman, then the hangman game is start
    if message.startswith("/hangman"):
        return dumps(hangman_start(token, channel_id, message))

    if message.startswith("/guess"):
        return dumps(hangman_guess(token, channel_id, message))

    return dumps(message_send(token, channel_id, message))

def hangman_start(token, channel_id, message):
    if channel_game_on(channel_id):
        raise InputError("an active game is already running for this channel")

    word_file = "/usr/share/dict/words"
    WORDS = open(word_file).read().splitlines()

    # RESET HANGMAN
    global HANGMAN_WORD
    global BOT_TOKEN
    global CORRECT_GUESSED
    global CORRECT_TIMES
    global WRONG_GUESS
    global GUESSED
    global HAVE_GUESSED
    global WRONG_TIMES

    HANGMAN_WORD = ""
    CORRECT_GUESSED.clear()
    WRONG_GUESS.clear()
    CORRECT_TIMES = 0
    WRONG_TIMES = 0
    GUESSED = ''
    HAVE_GUESSED.clear()

    HANGMAN_WORD = random.choice(WORDS)
    HANGMAN_WORD = HANGMAN_WORD.upper()

    word_to_guess = "_ " * len(HANGMAN_WORD)
    CORRECT_GUESSED = ["_"] * len(HANGMAN_WORD)

    out_message = (
        "Welcome to Hangman!\n"
        "Word: {}"
    ).format(word_to_guess)


    DATA = getData()

    for channel in DATA['channels']:
        if channel['channel_id'] == channel_id:
            target_channel = channel
    
    target_channel['game_on'] = True

    # create a hangman bot if it has not been created yet
    if BOT_TOKEN == "":
        DATA['users_count'] += 1
        generate_ID = DATA['users_count']

        hangman_bot = vars(User(generate_ID, "Hangman@bot.com", "Hangman", "Bot"))
        DATA['users'].append(hangman_bot)
        target_channel['members'].append(hangman_bot)

        BOT_TOKEN = str(generate_token(generate_ID))


    return message_send(BOT_TOKEN, channel_id, out_message)

def hangman_guess(token, channel_id, message):
    if not channel_game_on(channel_id):
        raise AccessError("The game has to be started before guessing")

    # message =  /guess X
    if not message[7].isalpha():
        raise InputError("The guess has to in the format: /guess X")

    DATA = getData()

    for channel in DATA['channels']:
        if channel['channel_id'] == channel_id:
            target_channel = channel

    guess = message[7].upper()

    global HAVE_GUESSED

    if guess in HAVE_GUESSED:
        raise InputError("You have guessed this letter before")

    HAVE_GUESSED.append(guess)

    global HANGMAN_WORD
    global BOT_TOKEN
    global CORRECT_GUESSED
    global WRONG_GUESS
    global CORRECT_TIMES
    global WRONG_TIMES
    global GUESSED

    if guess in HANGMAN_WORD:
        CORRECT_TIMES += 1
        index_list = []
        for index, item in enumerate(HANGMAN_WORD):
            if guess in item:
                index_list.append(index)

        for i in index_list:
            CORRECT_GUESSED[i] = guess

        list_to_string = ' '.join(str(elem) for elem in CORRECT_GUESSED)

        out_message = "Word: {} \n".format(list_to_string)

        if GUESSED != '':
            out_message += "You have guessed {} \n".format(GUESSED)

        if CORRECT_TIMES == len(set(HANGMAN_WORD)):
            out_message += "You won! \n"
            target_channel['game_on'] = False

            return message_send(BOT_TOKEN, channel_id, out_message)

        return message_send(BOT_TOKEN, channel_id, out_message)


    WRONG_TIMES += 1

    if WRONG_TIMES == 10:
        out_message = "You lost! \n"
        out_message += phases_list[10]

        target_channel['game_on'] = False

        return message_send(BOT_TOKEN, channel_id, out_message)

    WRONG_GUESS.append(guess)
    GUESSED = ' '.join(map(str, WRONG_GUESS))

    have_guessed_in_str = ' '.join(str(elem) for elem in CORRECT_GUESSED)

    out_message = (
        "Word: {} \n"
        "{} \n"
        "You have gussed {} \n"
    ).format(have_guessed_in_str, phases_list[WRONG_TIMES], GUESSED)

    return message_send(BOT_TOKEN, channel_id, out_message)

def message_send(token, channel_id, message):
    '''Send a message from authorised_user to the channel specified by channel_id'''

    DATA = getData()

    if len(message) > 1000:
        raise InputError('invalid message content')

    if not channel_member_check(channel_id, token):
        raise AccessError("Authorised user is not a member of channel with channel_id")

    # get message_id
    DATA['messages_count'] += 1
    message_id = DATA['messages_count']

    # get current time and send message
    now = datetime.datetime.utcnow()
    current_time = int(now.replace(tzinfo=datetime.timezone.utc).timestamp())
    DATA['messages'].append(vars(Message(message, message_id, channel_id, token_to_uid(token), int(current_time))))

    returnvalue = {} 
    returnvalue['message_id'] = message_id

    return returnvalue
