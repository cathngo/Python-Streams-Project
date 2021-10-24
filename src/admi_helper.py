from src.data_store import data_store
from src.error import InputError, AccessError

def change_permissions_helper(global_owner_id, u_id, permission_id):
    store = data_store.get()

    owners_count = 0
    new_global_found = False
    global_found = False
    for user in store['users']:
        if user['is_stream_owner'] == True:
            owners_count += 1
            if user['u_id'] == u_id: new_global_found = True
            if user['u_id'] == global_owner_id: global_found = True 

    if not global_found:   
        raise AccessError
    elif not new_global_found or (new_global_found == True and owners_count == 1):
        raise InputError
    elif permission_id != 1 and permission_id != 2:
        raise InputError

    
    for user in store['users']:
        if user['u_id'] == u_id:  
            user['is_stream_owner'] = True if permission_id == 1 else False
            data_store.set(store)