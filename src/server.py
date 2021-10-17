import sys
import signal
from json import dumps
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.error import InputError
from src import config
from src.other import clear_v1
from src.auth import auth_register_v1
from src.error import AccessError
from src.channels import channels_create_v1
from src.channel import channel_details_v1
from src.token_helper import decode_jwt, check_valid_token
from src.dm_create import dm_create_v1
from src.dm_list import dm_list_v1
from src.users_all_v1_helper import get_all_users

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

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

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

# Clear
@APP.route("/clear/v1", methods=['DELETE'])
def clear():
    clear_v1()
    return dumps({})

@APP.route("/auth/register/v2", methods=['POST'])
def auth_register_v2_http():
    data = request.get_json()
    return jsonify(
        auth_register_v1(data['email'], data['password'], data['name_first'], data['name_last'])
    )

#channels_create_v2
@APP.route("/channels/create/v2", methods=['POST'])
def create_channel():
    data = request.get_json()
    name = data['name']
    is_public = data['is_public']
    token = data['token']

    #check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    channel = channels_create_v1(user_token['u_id'], name, is_public)

    return dumps({
        'channel_id': channel['channel_id']
    })


#channel_details_v2
@APP.route("/channel/details/v2", methods=['GET'])
def get_channel_details():

    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))

    #check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    details = channel_details_v1(user_token['u_id'], channel_id)

    return dumps(
        details
    )

@APP.route("/dm/create/v1", methods=['POST'])
def create_new_dm():
    data = request.get_json()
    return jsonify(
        dm_create_v1(data['token'], data['u_ids'])
    )

@APP.route("/dm/list/v1", methods=['GET'])
def get_user_dms():
    data = request.get_json()
    return jsonify(
        dm_list_v1(data['token'])
    )

#users_all_v1
@APP.route("/users/all/v1", methods=['GET'])
def fetch_users():
    token = request.args.get('token')

     #check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    users = get_all_users()

    return dumps(users)


#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
