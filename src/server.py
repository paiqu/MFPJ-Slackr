import sys
from json import dumps
from flask import Flask, request, blueprints
from flask_cors import CORS
from error import InputError
from channels_create import CREATE
from channel_addowner import ADDOWNER
from channel_removeowner import RMVOWNER
from channel_join import JOIN

from class_file import User
from auth_register_route import REGISTER 
from auth_login import LOGIN 
from auth_logout import LOGOUT
from channel_invite import INVITE 
from channel_details import DETAILS
from user_permission import PERMISSION
from message_sendlater import SENDMESSAGELATER
from message_send import SENDMESSAGE
from message_remove import REMOVE
from message_pin import PIN
from message_unpin import UNPIN
from user_profile import PROFILE
from search import SEARCH
from channel_messages import CHANNEL_MESSAGES
from channels_list import CHANNELS_LIST
from channels_listall import CHANNELS_LISTALL
from message_edit import MESSAGE_EDIT
from message_react import MESSAGE_REACT
from message_unreact import MESSAGE_UNREACT
from user_setname import SETNAME
from user_setemail import SETEMAIL
from user_sethandle import SETHANDLE
from user_all import ALL
from standup_start import START
from standup_active import ACTIVE
from standup_send import SEND
from workspace_reset import RESET
from channel_join import JOIN
from channel_leave import LEAVE



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

APP.register_blueprint(LOGIN)
APP.register_blueprint(LOGOUT)
APP.register_blueprint(REGISTER)
APP.register_blueprint(INVITE)
APP.register_blueprint(DETAILS)
APP.register_blueprint(CHANNEL_MESSAGES)
APP.register_blueprint(LEAVE)
APP.register_blueprint(JOIN)
APP.register_blueprint(ADDOWNER)
APP.register_blueprint(RMVOWNER)
APP.register_blueprint(CHANNELS_LIST)
APP.register_blueprint(CHANNELS_LISTALL)
APP.register_blueprint(CREATE)
APP.register_blueprint(SENDMESSAGE)
APP.register_blueprint(SENDMESSAGELATER)
APP.register_blueprint(MESSAGE_REACT)
APP.register_blueprint(MESSAGE_UNREACT)
APP.register_blueprint(PIN)
APP.register_blueprint(UNPIN)
APP.register_blueprint(REMOVE)
APP.register_blueprint(MESSAGE_EDIT)
APP.register_blueprint(PROFILE)
APP.register_blueprint(SETNAME)
APP.register_blueprint(SETEMAIL)
APP.register_blueprint(SETHANDLE)
APP.register_blueprint(ALL)
APP.register_blueprint(SEARCH)
APP.register_blueprint(START)
APP.register_blueprint(ACTIVE)
APP.register_blueprint(SEND)
APP.register_blueprint(PERMISSION)
APP.register_blueprint(RESET)


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
