from src.data_store import data_store
from src.token_helper import decode_jwt, check_valid_token
from src.dm_helper import check_dm_id_exists, check_user_in_dm, obtain_user_details
from src.data_persistence import save_pickle, open_pickle

'''
Given a DM with ID dm_id that the authorised user is a member of,
provide basic details about the DM.

Arguments:
    token (string) - user's token
    dm_id (integer) - unique id of a DM

Exceptions:
    InputError - dm_id does not refer to a valid DM
    AccessError - Occurs when any of:
        - Invalid token is passed through
        - dm_id is valid and the authorised user is not a member of the DM

Return Value:
    Returns a dictionary containing the name of the DM and a list of members in the DM
'''
def dm_details_v1(token, dm_id):
    store = open_pickle()

    # Check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    # Check if dm_id refers to a valid DM
    dm_check = check_dm_id_exists(dm_id, store)

    # Check if authorised user is a member of the DM
    check_user_in_dm(user_token['u_id'], dm_check)

    # List of dictionaries to store user details
    members = []

    for member_iter in dm_check['members']:
        members.append(obtain_user_details(member_iter, store))

    return {
        'name': dm_check['name'],
        'members': members,
    }