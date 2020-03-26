# Route implementation for channels/route
from json import dumps
from flask import Blueprint, request
from data import DATA, getData

LEAVE = Blueprint('channels_listall', __name__)

@LEAVE.route('/channels/listall', methods=['POST'])
def listall():
    # function for route channels/list
    token = request.args.get('token')
    return dumps(channels_list(token, channel_id))
    
def channels_listall(token):
    '''
    Given a token, list all channels 
    
    '''
    
    global DATA
    DATA = getData()
    return DATA['channels']
