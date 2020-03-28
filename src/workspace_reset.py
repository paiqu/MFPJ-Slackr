from json import dumps
from flask import Blueprint, request
from data import DATA



WORKSPACERESET = Blueprint('workspace_reset', __name__)

@WORKSPACERESET.route('/workspace/reset', methods=['POST'])
def workspace_reset():

    
    global DATA
    
    DATA = {
        'users': [],
        'channels': [],
        'messages': []
    }
    

    return dumps({})