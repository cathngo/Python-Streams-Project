from src.data_store import data_store
from src.token_helper import decode_jwt, check_valid_token
from src.dm_helper import check_dm_id_exists, check_user_is_dm_owner

def dm_remove_v1(token, dm_id):
    '''
    Remove an existing DM, so all members are no longer in the DM. This can only be done by the original creator of the DM.
    '''
    store = data_store.get()

    # Check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    # Check if dm_id refers to a valid DM
    dm_check = check_dm_id_exists(dm_id, store)

    # Check if authorised user is a member of the DM
    check_user_is_dm_owner(user_token['u_id'], dm_check)

    # Create new dm list which does not contain the removed DM
    new_dm_list = [dm_dict for dm_dict in store['dm'] if dm_dict.get('dm_id') != dm_id]
    store['dm'] = new_dm_list

    data_store.set(store)

    return {}