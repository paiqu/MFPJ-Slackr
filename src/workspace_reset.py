from json import dumps
from flask import Blueprint, request
from data import DATA



RESET = Blueprint('workspace_reset', __name__)

@RESET.route('/workspace/reset', method=['POST'])
def reset():
    global DATA
    DATA = {
        'users': [],
        'channels': [],
        'messages': []
    }

    return dumps({})
