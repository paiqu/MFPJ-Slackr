import sys
from json import dumps
from flask import Flask, request, blueprints
from flask_cors import CORS
from error import InputError, AccessError
from channels_create import CREATE
from class_file import User

from channel_messages import CHANNEL_MESSAGES
from channels_list import CHANNELS_LIST
from channels_listall import CHANNELS_LISTALL
from message_edit import MESSAGE_EDIT
from message_react import MESSAGE_REACT
#from message_unreact import MESSAGE_UNREACT

'''
def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response
'''
APP = Flask(__name__)
CORS(APP)

'''
APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)
'''
APP.register_blueprint(CREATE)
APP.register_blueprint(CHANNEL_MESSAGES)
APP.register_blueprint(CHANNELS_LIST)
APP.register_blueprint(CHANNELS_LISTALL)
APP.register_blueprint(MESSAGE_EDIT)
APP.register_blueprint(MESSAGE_REACT)
#APP.register_blueprint(MESSAGE_UNREACT)
# Example

@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 8080))
