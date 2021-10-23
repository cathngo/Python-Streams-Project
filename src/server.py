import sys
import signal
from json import dumps
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.error import InputError
from src import config
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1, auth_logout_v1
from src.error import AccessError
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.channel import channel_details_v1, messages_channel_v1, messages_dm_v1, channel_join_v1, channel_leave_v1, channel_addowner_v1
from src.token_helper import decode_jwt, check_valid_token
from src.dm_create import dm_create_v1
from src.dm_list import dm_list_v1
from src.dm_details import dm_details_v1
from src.dm_remove import dm_remove_v1
from src.dm_leave import dm_leave_v1
from src.users_all_v1_helper import get_all_users
from src.user_profile_v1_helper import get_user_profile, check_valid_u_id
from src.user_profile_put_helpers import set_username, set_handle, set_email
from src.send_message import message_send_channel, message_send_dm

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

#auth_login_v2
@APP.route("/auth/login/v2", methods=['POST'])
def auth_login_v2_http():
    data = request.get_json()
    login_return = auth_login_v1(data['email'], data['password'])
    return dumps({
        'token': login_return['token'],
        'auth_user_id': login_return['auth_user_id'],
    })

#auth_logout_v1
@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout_v1_http():
    data = request.get_json()
    token = data['token']
    user_token = decode_jwt(token)
    session_id = user_token['session_id']
    auth_logout_v1(session_id)
    return dumps({})

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

#channels_list_v2
@APP.route("/channels/list/v2", methods=['GET'])
def get_list_channels():
    token = request.args.get('token')
    #decode and check if valid
    user_token = decode_jwt(token)
    check_valid_token(user_token)
    
    return dumps(
        channels_list_v1(user_token['u_id'])
    )

#channels_listall_v2
@APP.route("/channels/listall/v2", methods=['GET'])
def get_listall_channels():
    token = request.args.get('token')
    #decode and check if valid
    user_token = decode_jwt(token)
    check_valid_token(user_token)
    
    return dumps(
        channels_listall_v1(user_token['u_id'])
    )
 
# Route function for channel_join_v2
@APP.route("/channel/join/v2", methods=['POST'])
def channel_join():
    data = request.get_json()
    user_token = data['token']
    token = decode_jwt(user_token)
    check_valid_token(token)
    channel_join_v1(token['u_id'], data['channel_id'])
    return dumps({})

# Route function for channel_leave_v2
@APP.route("/channel/leave/v1", methods=['POST'])
def channel_leave():
    data = request.get_json()
    user_token = data['token']
    token = decode_jwt(user_token)
    check_valid_token(token)
    channel_leave_v1(token['u_id'], data['channel_id'])
    return dumps({})


# Route function for channel_addowner_v1
@APP.route("/channel/addowner/v1", methods=['POST'])
def channel_addowner():
    data = request.get_json()
    user_token = data['token']
    token = decode_jwt(user_token)
    check_valid_token(token)
    channel_addowner_v1(token['u_id'], data['channel_id'], data['u_id'])
    return dumps({})

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
    token = request.args.get('token')

    dms_list = dm_list_v1(token)

    return dumps(dms_list)

@APP.route("/dm/remove/v1", methods=['DELETE'])
def remove_dm():
    data = request.get_json()

    dm_remove_v1(data['token'], data['dm_id'])

    return dumps({})

@APP.route("/dm/details/v1", methods=['GET'])
def get_dm_details():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))

    dm_details_output = dm_details_v1(token, dm_id)

    return dumps(dm_details_output)

@APP.route("/dm/leave/v1", methods=['POST'])
def leave_dm():
    data = request.get_json()
    
    dm_leave_v1(data['token'], data['dm_id'])
    
    return dumps({})

#users_all_v1
@APP.route("/users/all/v1", methods=['GET'])
def fetch_users():
    token = request.args.get('token')

     #check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    users = get_all_users()

    return dumps(users)

#user_profile_v1
@APP.route("/user/profile/v1", methods=['GET'])
def fetch_user_profile():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))

    #check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    #check valid u_id
    check_valid_u_id(u_id)

    user_profile = get_user_profile(token, u_id)

    return dumps(user_profile)

#user_profile_setname_v1
@APP.route("/user/profile/setname/v1", methods=['PUT'])
def update_user_names():
    data = request.get_json()
    first_name = data['name_first']
    last_name = data['name_last']
    token = data['token']

    #check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    set_username(user_token['u_id'], first_name, last_name)
    return dumps({})

#user_profile_sethandle_v1
@APP.route("/user/profile/sethandle/v1", methods=['PUT'])
def update_user_handle():
    data = request.get_json()
    handle_str = data['handle_str']
    token = data['token']

    #check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    set_handle(user_token['u_id'], handle_str)

    return dumps({})

@APP.route("/channel/messages/v2", methods=['GET'])
def get_channel_message():

    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))

    #check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    messages_channel = messages_channel_v1(user_token['u_id'], channel_id, start)
   
    return dumps(
        messages_channel
    )

#user_profile_setemail_v1
@APP.route("/user/profile/setemail/v1", methods=['PUT'])
def update_user_email():
    data = request.get_json()
    email = data['email']
    token = data['token']
    
    user_token = decode_jwt(token)
    check_valid_token(user_token)
    
    set_email(user_token['u_id'], email)
    
    return dumps({})

@APP.route("/dm/messages/v1", methods=['GET'])
def get_dm_messages():
    token = request.args.get('token')
    dm_id = int(request.args.get('dm_id'))
    start = int(request.args.get('start'))
    
    #check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    messages_dm = messages_dm_v1(user_token['u_id'], dm_id, start)
    
    return dumps(
        messages_dm
    )

@APP.route("/message/send/v1", methods=['POST'])
def post_send_message():
    data = request.get_json()
    
    token = data['token']
    channel_id = data['channel_id']
    message = data['message']
    
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    return dumps(
        message_send_channel(user_token['u_id'], channel_id, message)
    )

@APP.route("/message/senddm/v1", methods=['POST'])
def post_send_message_dm():
    data = request.get_json()
    
    token = data['token']
    dm_id = data['dm_id']
    message = data['message']
    
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    return dumps(
        message_send_dm(user_token['u_id'], dm_id, message)
    )

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
