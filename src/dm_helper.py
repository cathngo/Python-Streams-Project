from src.channels_invite_helper import check_u_id_exists

def check_valid_u_id_list(u_ids, store):
    '''
    Check if any u_id in u_ids does not refer to a valid user
    Returns InputError if u_ids is empty
    '''
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

def generate_dm_names(u_ids, store):
    '''
    Creates a list of names for users in dm
    Don't need to check if user id in u_ids exists or not
    '''
    new_dm_list = []
    for id in u_ids:
        new_dm_list.append(find_user_handle(id, store))
    new_dm_list.sort()
    return new_dm_list