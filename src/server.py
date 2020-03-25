import sys
from json import dumps
from flask import Flask, request, blueprints
from flask_cors import CORS
from error import InputError
from channels_create import CREATE
from channel_addowner import ADDOWNER
from channel_removeowner import RMVOWNER
from class_file import User

from channel_leave import LEAVE

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
APP.register_blueprint(ADDOWNER)
APP.register_blueprint(RMVOWNER)

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
