from json import dumps
from flask import Blueprint, request
from data import DATA, CHANNELS_COUNT, MESSAGE_COUNT



RESET = Blueprint('workspace_reset', __name__)

@RESET.route('/workspace/reset', methods=['POST'])
def reset():
    global DATA
    DATA['users'].clear()
    DATA['channels'].clear()
    DATA['messages'].clear()
    DATA['reacts'].clear()
    DATA['standups'].clear()
    DATA['users_count'] = 0
    DATA['channels_count'] = 0
    DATA['messages_count'] = 0
   
    # global CHANNELS_COUNT
    # CHANNELS_COUNT = 0

    # global MESSAGE_COUNT
    # MESSAGE_COUNT = 0
    

    return dumps({})
