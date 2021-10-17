from src.data_store import data_store
from src.auth_register_helper import check_name
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