from src.data_store import data_store
from src.token_helper import decode_jwt, check_valid_token
from src.dm_helper import check_dm_id_exists, check_user_in_dm, obtain_user_details

def dm_details_v1(token, dm_id):
    '''
    Given a DM with ID dm_id that the authorised user is a member of,
    provide basic details about the DM.
    '''
    store = data_store.get()

    # Check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    # Check if dm_id refers to a valid DM
    dm_check = check_dm_id_exists(dm_id, store)

    # Check if authorised user is a member of the DM
    check_user_in_dm(user_token['u_id'], dm_id, store)

    # List of dictionaries to store user details
    members = []

    for user in dm_check['members']:
        members.append(obtain_user_details(user, store))

    return {
        'name': dm_check['name'],
        'members': members,
    }