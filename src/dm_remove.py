from src.data_store import data_store
from src.token_helper import decode_jwt, check_valid_token
from src.dm_helper import check_dm_id_exists, check_user_is_dm_owner
from src.data_persistence import save_pickle, open_pickle
from src.users_stats_helper import update_dms_exist, update_messages_exist
from src.user_stats_helper import update_dms_joined


def dm_remove_v1(token, dm_id):
    '''
    Remove an existing DM, so all members are no longer in the DM.
    This can only be done by the original creator of the DM.

    Arguments:
        token (string) - user's token
        dm_id (integer) - unique id of a DM

    Exceptions:
        InputError - dm_id does not refer to a valid DM
        AccessError - Occurs when any of:
            - Invalid token is passed through
            - dm_id is valid and the authorised user is not the original DM creator

    Return Value:
        Returns an empty dictionary 
        '''

    store = open_pickle()

    # Check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    # Check if dm_id refers to a valid DM
    dm_check = check_dm_id_exists(dm_id, store)

    # Check if authorised user is a member of the DM
    check_user_is_dm_owner(user_token['u_id'], dm_check)


    #user stats 
    dm_rem = {}
    for dm in store['dm']:
        if dm['dm_id'] == dm_id:
            dm_rem = dm
        #find all users in the dm
            for id in dm['members']:
                #decrement number of dms joined for the user's stats by one
                update_dms_joined(id, store, -1)

    #decrement number of msgs for workspace stats depending on number msgs in the dm removed
    num_msgs = len(dm_rem['messages'])

    update_messages_exist(store, -num_msgs)

    #decrement number of existing dms for workspace stats by one
    update_dms_exist(store, -1)

    # Create new dm list which does not contain the removed DM
    new_dm_list = [dm_dict for dm_dict in store['dm'] if dm_dict.get('dm_id') != dm_id]
    store['dm'] = new_dm_list

    data_store.set(store)
    save_pickle()


    return {}
