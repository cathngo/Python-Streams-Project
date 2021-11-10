from src.token_helper import decode_jwt, check_valid_token
from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
import os
from src import config
from urllib.request import urlopen

def check_default(user_id):
    #check if they have uploaded a profile pic
    success = True
    try:
        urlopen(config.url + 'static/' + str(user_id) + '.jpg')
    except:
        success = False
    
    #if they haven't set the profile img url to default img
    if success == False:
        return config.url + 'static/default.jpg'
    else:
        return config.url + 'static/' + str(user_id) + '.jpg'
    

def get_all_users():  
    store = open_pickle()
    path = os.path.join(current_app.root_path, 'images')

    all_users = []
    #check all the users in the database
    for user in store['users']:
        if user['handle_str'] != '':
            temp_dict = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'], 
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],
                'profile_img_url': user['profile_img_url']
            }
            all_users.append(temp_dict)
    return {
        'users': all_users
    }
