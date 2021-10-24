from src.data_store import data_store
from src.token_helper import decode_jwt, check_valid_token
from src.dm_helper import check_dm_id_exists, check_user_in_dm
from src.data_persistence import save_pickle, open_pickle

'''
Given a DM ID, the user is removed as a member of this DM.
The creator is allowed to leave and the DM will still exist if this happens.
This does not update the name of the DM.

Arguments:
    token (string) - user's token
    dm_id (integer) - unique id of a DM

Exceptions:
    InputError - dm_id does not refer to a valid DM
    AccessError - Occurs when any of:
        - Invalid token is passed through
        - dm_id is valid and the authorised user is not a member of the DM

Return Value:
    Returns an empty dictionary
'''
def dm_leave_v1(token, dm_id):
    store = open_pickle()

    # Check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    # Check if dm_id refers to a valid DM
    dm_check = check_dm_id_exists(dm_id, store)

    # Check if authorised user is a member of the DM
    check_user_in_dm(user_token['u_id'], dm_check)

    # Create new member list which does not contain the removed user
    new_member_list = [dm_member for dm_member in dm_check['members'] if dm_member != user_token['u_id']]
    for dm_iter in store['dm']:
        if dm_iter['dm_id'] == dm_id:
            dm_iter['members'] = new_member_list

    data_store.set(store)
    save_pickle()

    return {}
