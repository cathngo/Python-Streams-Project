from src.token_helper import decode_jwt, check_valid_token
from src.data_store import data_store

def get_user_profile(token, u_id):
    store = data_store.get()
    #check valid token

    user_profile = {}
    for user in store['users']:
        if user['u_id'] == token['u_id']:
            user_profile = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'], 
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
            }
            return user_profile

    return AccessError("User does not exist")