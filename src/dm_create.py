from src.data_store import data_store
from src.dm_helper import check_valid_u_id_list, generate_dm_id, generate_dm_names
from src.token_helper import decode_jwt, check_valid_token
from src.data_persistence import save_pickle, open_pickle
from src.user_stats_helper import update_dms_joined
from src.users_stats_helper import update_dms_exist
from src.notifications import identify_add

def dm_create_v1(token, u_ids):
    '''
Creates a dm based on input and returns a unique dm id

Arguments:
    token (string) - user's token
    u_ids (list) - contains the user(s) that this DM is directed to, and will not include the creator

Exceptions:
    InputError - any u_id in u_ids does not refer to a valid user
    AccessError - Invalid token is passed through

Return Value:
    Returns a dictionary containing a unique dm_id
'''
    store = open_pickle()

    # Check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    # Check for valid users
    check_valid_u_id_list(u_ids, store)

    # Generate new dm_id
    dm_id = generate_dm_id()

    # Generate name for dm
    dm_name = generate_dm_names(u_ids, store, user_token['u_id'])
    original_uids = u_ids.copy()
    # Populate users in the dm into a list
    dm_members = u_ids
    dm_members.append(user_token['u_id'])

    store['dm'].append({
        'dm_id': dm_id,
        'name': dm_name,
        'owner_id': user_token['u_id'],
        'members': dm_members,
        'messages': [],
    })
    data_store.set(store)
    save_pickle()    

    for dude in original_uids:
        identify_add(user_token['u_id'], dude, -1, dm_id)

    store = open_pickle()

    #increment number of dms joined for the user's stats by one
    for id in u_ids:
        update_dms_joined(id, store, 1)
 
    store = open_pickle()

    #increment total number of existing dms by one for workspace stats
    update_dms_exist(store, 1)
    data_store.set(store)
    save_pickle()    

    return {
        'dm_id': dm_id
    }
