from src.channels_invite_helper import check_u_id_exists
from src.error import InputError, AccessError

def check_valid_u_id_list(u_ids, store):
    '''
    Check if any u_id in u_ids does not refer to a valid user
    Skips check if u_ids is empty
    '''
    if not u_ids:
        return

    for id in u_ids:
        check_u_id_exists(id, store)

NEW_DM_ID = 0
def generate_dm_id():
    '''
    Create new unique dm_id
    '''
    global NEW_DM_ID
    NEW_DM_ID += 1
    return NEW_DM_ID

def find_user_handle(u_id, store):
    '''
    Returns the user's handle in the data store
    '''
    for user in store['users']:
        if user['u_id'] == u_id:
            return user['handle_str']

def generate_dm_names(u_ids, store, owner_id):
    '''
    Creates a list of names for users in dm
    Don't need to check if user id in u_ids exists or not
    Owner of DM is added to name
    '''
    owner_handle = find_user_handle(owner_id, store)
    new_dm_list = [owner_handle]

    for id in u_ids:
        new_dm_list.append(find_user_handle(id, store))
    new_dm_list.sort()

    # Convert to a string
    dm_name = ', '.join(new_dm_list)
    return dm_name

def check_dm_id_exists(dm_id, store):
    '''
    Checks in the data store if the given dm_id exists
    Returns the DM if it exists
    '''
    for dm_iter in store['dm']:
        if dm_iter['dm_id'] == dm_id:
            return dm_iter
    raise InputError(description='dm_id does not exist')

def check_user_in_dm(auth_user_id, dm_check):
    '''
    Checks if the user is a member of the given dm
    '''
    for user_iter in dm_check['members']:
        if auth_user_id == user_iter:
            return
    raise AccessError(description='authorised user is not a member of the DM')

def obtain_user_details(auth_user_id, store):
    '''
    Returns a dictionary containing user details
    Assumes u_id is a valid and existing id in data store
    '''
    for user_iter in store['users']:
        if auth_user_id == user_iter['u_id']:
            user_details_temp = {
                'u_id': user_iter['u_id'],
                'email': user_iter['email'],
                'name_first': user_iter['name_first'], 
                'name_last': user_iter['name_last'],
                'handle_str': user_iter['handle_str'],
            }
            return user_details_temp

def check_user_is_dm_owner(auth_user_id, dm_check):
    '''
    Checks if the user is the dm owner
    '''
    if auth_user_id == dm_check['owner_id']:
        return
    raise AccessError(description='authorised user is not a member of the DM')