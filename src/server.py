import sys
from json import dumps
from flask import Flask, request, blueprints
from flask_cors import CORS
from error import InputError
from channels_create import CREATE
from class_file import User
from message_sendlater import SENDMESSAGELATER
from message_send import SENDMESSAGE
from message_remove import REMOVE
from message_pin import PIN
from message_unpin import UNPIN
from user_profile import PROFILE
from search import SEARCH

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

APP = Flask(__name__)
CORS(APP)


APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

APP.register_blueprint(CREATE)
APP.register_blueprint(UNPIN)
APP.register_blueprint(PIN)
APP.register_blueprint(REMOVE)
APP.register_blueprint(SENDMESSAGE)
APP.register_blueprint(SENDMESSAGELATER)
APP.register_blueprint(PROFILE)
APP.register_blueprint(SEARCH)

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
