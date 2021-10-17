from src.data_store import data_store
from src.token_helper import decode_jwt, check_valid_token

def dm_list_v1(token):
    '''
    Returns the list of DMs that the user is a member of
    '''
    store = data_store.get()

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