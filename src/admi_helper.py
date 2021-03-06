from src.data_store import data_store
from src.error import InputError, AccessError
from src.data_persistence import save_pickle, open_pickle



def change_permissions_helper(global_owner_id, u_id, permission_id):
    '''
Changes the permissions of an user from the Stream, the new permissions are
decided by 'permission_id'

Arguments:
    token (string) - user's token
    u_id (integer) - unique id of an user
    permision_id (integer) - decides which what permission we want to change into

Exceptions:
    InputError - u_id does not refer to a valid user
    InputError - u_id refers to a user who is the only global owner
    InputError - permission_id is not 1 or 2
    AccessError - Occurs when any of:
        - Invalid token is passed through.
        - The authorised user is not a global owner.

Return Value:
    Returns an empty dictionary
'''

    store = open_pickle()

    #check if the u_id is a streams owner if they are a streams owner 
    #check if the person receiving the invitation is a streams owner 
    
    new_global_found = False
    global_found = False
    #count how many global owners there are this cannot, be zero at the end of this function
    owners_count = 0 
    for user in store['users']:
        if user['is_streams_owner'] == True:
            owners_count += 1
        if user['u_id'] == u_id: 
            new_global_found = True
        if user['u_id'] == global_owner_id and user['is_streams_owner'] == True: 
            global_found = True 

    if not global_found:   
        raise AccessError(description='The authorised user is not a global owner.')
    elif not new_global_found or (new_global_found == True and owners_count == 1 and permission_id == 2):
       raise InputError(description='Invalid u_id.')
    elif permission_id != 1 and permission_id != 2:
        raise InputError(description='Invalid permission_id.')

    
    for user in store['users']:
        if user['u_id'] == u_id: 
            if permission_id == 1:
                user['is_streams_owner'] = True 
            else:
                user['is_streams_owner'] = False
    data_store.set(store)
    save_pickle()