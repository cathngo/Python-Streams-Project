from src.data_store import data_store
from src.token_helper import decode_jwt, check_valid_token
from src.data_persistence import save_pickle, open_pickle

'''
Returns the list of DMs that the user is a member of

Arguments:
    token (string) - user's token

Exceptions:
    AccessError - Occurs when any of:
        - Invalid token is passed through

Return Value:
    Returns a dictionary containing dms, which is a list of dictionaries,
    where each dictionary contains types { dm_id, name }
'''
def dm_list_v1(token):
    store = open_pickle()

    # Check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    joined_dms = []
    
    # Search the data store for DMs and append it to joined_dms if user is a member
    for dm_iter in store['dm']:
        for member in dm_iter['members']:
            if member == user_token['u_id']:
                joined_dms.append({
                    'dm_id': dm_iter['dm_id'],
                    'name': dm_iter['name'],
                })

    return {
        'dms': joined_dms,
    }
