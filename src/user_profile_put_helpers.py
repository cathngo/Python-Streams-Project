from src.data_store import data_store
from src.auth_register_helper import check_name, check_duplicate_handle, check_email, check_duplicate_email
from src.error import AccessError
from src.error import InputError
from src.data_persistence import save_pickle, open_pickle
'''
Updates the authorised user's first and last name 

Arguments:
    auth_user_id (int) - the target user's id to apply updates to
    name_first (string) - the user's first name after the update
    name_last (string) - the user's last name after the update

Exceptions:
InputError - Occurs when:
    - The length of name_first is not between 1 and 50 characters inclusive
    - the length of name_last is notbetween 1 and 50 characters inclusive

Return Value:
    Does not return anything
'''

def set_username(auth_user_id, name_first, name_last):

    store = open_pickle()
    #check name between 1 and 50 ch
    check_name(name_first)
    #check last name between 1 and 50 ch
    check_name(name_last)

    for user in store['users']:
        if user['u_id'] == auth_user_id:
            user['name_first'] = name_first
            user['name_last'] = name_last
    data_store.set(store)
    save_pickle()
'''
Updates the authorised user's handle (i.e display name)

Arguments:
    auth_user_id (int) - the target user's id to apply updates to
    handle_str (string) - the user's handle after the update

Exceptions:
InputError - Occurs when:
    - The length of handle_str is not between 3 and 20 characters inclusive
    - handle_str contains characters that are not alphanumeric
    - the handle is already used by another user

Return Value:
    Does not return anything
'''

def set_handle(auth_user_id, handle_str):

    store = open_pickle()
    #check handle_str between 3 and 20 ch
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description='Invalid handle length')
    #check handle_str contains alphanumeric ch only
    if handle_str.isalnum() == False:
        raise InputError(description='Non alphanumeric handle')

    #check duplicate handle str
    if check_duplicate_handle(handle_str, store) == True:
        raise InputError(description='Handle already exists')

    for user in store['users']:
        if user['u_id'] == auth_user_id:
            user['handle_str'] = handle_str 

    data_store.set(store)
    save_pickle()

'''
Updates the authorised email

Arguments:
    auth_user_id (int) - the target user's id to apply updates to
    email (string) - the user's email after the update

Exceptions:
InputError - Occurs when:
    - email is not a valid email 
    - email address is already being used by another user

Return Value:
    Does not return anything
'''

def set_email(auth_user_id, email):

    store = open_pickle()
    #check email valid
    check_email(email)
    #check duplicate email
    check_duplicate_email(email, store) 

    for user in store['users']:
        if user['u_id'] == auth_user_id:
            user['email'] = email
    
    data_store.set(store)
    save_pickle()
