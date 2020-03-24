'''Route implementation for message'''
from json import dumps
from flask import Blueprint, request
from check_functions import token_to_uid
from error import InputError
from class_file import User
from data import DATA, getData

MESSAGE = Blueprint('message', __name__)


@MESSAGE.route('/send', methods=['Post'])
def request_get():
    '''request get for route message send'''
    request = request.get_json()
    token = request['token']
    channel_id = request['channel_id']
    message_content = request['message']
    
    message_send(token, channel_id, message_content)
    return dumps({})

