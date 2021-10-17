from src.token_helper import decode_jwt, check_valid_token
from src.data_store import data_store

def get_all_users(token_user):  
    store = data_store.get()
    #check valid token
    check_valid_token(token_user)

    all_users = []
    #check all the userese in the database
    for user in store['users']:
        temp_dict = {
            'u_id': user['u_id'],
            'email': user['email'],
            'name_first': user['name_first'], 
            'name_last': user['name_last'],
            'handle_str': user['handle_str'],

		}
        all_users.append(temp_dict)
    
    return {
        'users': all_users
    }
