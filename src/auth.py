from src.data_store import data_store
from src.error import InputError
from src.auth_register_helper import check_email, check_duplicate_email, check_password, check_name, create_handle

def auth_login_v1(email, password):
    
    store = data_store.get()
    
    # Checks that the email is valid 
    check_email(email)
     
    # Checks if email and password are correct
    # Returns auth_user_id
    for user in store['users']:
        if user['email'] == email:
            if user['password'] == password:
                return {
                    'auth_user_id': user['u_id']
                }
            else:
                raise InputError('Error: Incorrect password')
    raise InputError('Error: Email entered does not belong to a user')
    
def auth_register_v1(email, password, name_first, name_last):
    store = data_store.get()

    # Checks user details for validity
    check_email(email)
    check_duplicate_email(email, store)
    check_password(password)
    check_name(name_first)
    check_name(name_last)

    u_id = len(store['users'])

    # First user to register becomes the streams owner
    is_streams_owner = True if (u_id == 0) else False
    
    # Creates unique handle
    handle_str = create_handle(name_first, name_last, store)
    
    # Registers user into store
    store['users'].append(
        {
            'u_id': u_id,
            'email': email,
            'password': password,
            'name_first': name_first, 
            'name_last': name_last,
            'handle_str': handle_str,
            'is_streams_owner': is_streams_owner,
        }
    )

    data_store.set(store)
    
    return {
        'auth_user_id': u_id
    }
