from src.token_helper import decode_jwt, check_valid_token
from src.data_store import data_store
from src.error import AccessError
from src.error import InputError
from src.data_persistence import save_pickle, open_pickle
from flask import current_app
import os
from src import config

def get_user_profile(token, user_id):
    store = open_pickle()
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
                'profile_img_url': config.url + 'static/' + str(user_id) + '.jpg'
            }
    return {'user': user_profile}


def check_valid_u_id(auth_user_id):
    store = open_pickle()

    found = False
    #search for u_id in users
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            found = True
    if found == False:
        raise InputError(description='Invalid user - could not find u_id')
