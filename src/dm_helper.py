from src.channels_invite_helper import check_u_id_exists

def check_valid_u_id_list(u_ids, store):
    '''
    Check if any u_id in u_ids does not refer to a valid user
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

def generate_dm_names(u_ids, store):
    '''
    Creates a list of names for users in dm
    '''