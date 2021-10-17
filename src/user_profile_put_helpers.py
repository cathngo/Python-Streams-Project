from src.data_store import data_store
from src.auth_register_helper import check_name, check_duplicate_handle
from src.error import AccessError
from src.error import InputError


def set_username(auth_user_id, name_first, name_last):
    store = data_store.get()
    #check name between 1 and 50 ch
    check_name(name_first)
    #check last name between 1 and 50 ch
    check_name(name_last)

    for user in store['users']:
        if user['u_id'] == auth_user_id:
            user['name_first'] = name_first
            user['name_last'] = name_last
            return 
    raise AccessError("User not found cannot update name")

def set_handle(auth_user_id, handle_str):
    store = data_store.get()
    #check handle_str between 3 and 20 ch
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError(description='Invalid handle length')
    #check handle_str contains alphanumeric ch only
    if handle_str.isalnum() == False:
        raise InputError(description='Non alphanumeric handle')

    #check duplicate handle str
    if check_duplicate_handle(handle_str, store) == True:
        raise InputError("Handle already exists")

    for user in store['users']:
        if user['u_id'] == auth_user_id:
            user['handle_str'] = handle_str
            return 
    return  