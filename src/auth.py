from src.data_store import data_store
from src.error import InputError
from src.auth_register_helper import check_email, check_duplicate_email, check_password, check_name, create_handle

def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }

def auth_register_v1(email, password, name_first, name_last):
    store = data_store.get()

    # Checks user details for validity
    check_email(email)
    check_duplicate_email(email, store)
    check_password(password)
    check_name(name_first)
    check_name(name_last)

    auth_user_id = len(store['users'])

    # First user to register becomes the streams owner
    is_streams_owner = True if (auth_user_id == 0) else False
    
    # Creates unique handle
    handle = create_handle(name_first, name_last, store)
    
    # Registers user into store
    store['users'].append(
        {
            'auth_user_id': auth_user_id,
            'email': email,
            'password': password,
            'name_first': name_first, 
            'name_last': name_last,
            'handle': handle,
            'is_streams_owner': is_streams_owner,
        }
    )
    
    return {
        'auth_user_id': auth_user_id
    }