from src.data_store import data_store
from src.error import InputError
from src.auth_register_helper import (
    check_email,
    check_duplicate_email,
    check_password,
    check_name,
    create_handle,
    generate_jwt,
    hash_user_password,
    generate_new_session_id,
)

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


'''
Registers a new user into the datastore

Arguments:
    email (string) - user's email
    password (string) - user's password
    name_first (string) - user's first name
    name_last (string) - user's last name

Exceptions:
    InputError - Occurs when any of:
        - invalid email entered
        - email entered is already in use
        - password length < 6 characters
        - length of name_first is not between 1 and 50 characters inclusive
        - length of name_last is not between 1 and 50 characters inclusive

Return Value:
    Returns a dictionary containing a unique token and auth_user_id
    if user is successfully registered into the datastore
'''
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

    # Hash user's input password
    password = hash_user_password(password)

    # Get new session id for user
    new_session_id = generate_new_session_id()

    # Creates unique token
    token = generate_jwt(u_id, new_session_id)
    
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
            'session_list': [new_session_id]
        }
    )

    data_store.set(store)
    
    return {
        'token': token,
        'auth_user_id': u_id
    }