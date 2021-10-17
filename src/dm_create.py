from src.data_store import data_store
from src.dm_helper import check_valid_u_id_list, generate_dm_id, generate_dm_names
from src.token_helper import decode_jwt, check_valid_token

def dm_create_v1(token , u_ids):
    '''
    Creates a dm based on input and returns a unique dm id
    '''
    store = data_store.get()

    # Check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    # Check for valid users
    check_valid_u_id_list(u_ids, store)

    # Generate new dm_id
    dm_id = generate_dm_id()

    # Generate name for dm
    dm_name = generate_dm_names(u_ids, store, user_token['u_id'])

    # Populate users in the dm into a list
    dm_members = u_ids
    dm_members.append(user_token['u_id'])

    store['dm'].append({
        'dm_id': dm_id,
        'name': dm_name,
        'owner_id': user_token['u_id'],
        'members': dm_members,
    })

    data_store.set(store)

    return {
        'dm_id': dm_id
    }