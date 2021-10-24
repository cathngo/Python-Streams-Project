from src.token_helper import decode_jwt, check_valid_token
from src.data_store import data_store
from src.error import AccessError
from src.error import InputError

def get_user_profile(token, user_id):
    store = data_store.get()
    #check valid token

    user_profile = {}
    for user in store['users']:
        if user['u_id'] == user_id:
            user_profile = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'], 
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
            }
    return user_profile


def check_valid_u_id(auth_user_id):
    store = data_store.get()

    found = False
    #search for u_id in users
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            found = True
    if found == False:
        raise InputError("Invalid user - could not find u_id")