from src.dm_helper import check_valid_u_id_list, generate_dm_id, generate_dm_names
#from src.token_helper import decode_jwt, check_valid_token

def dm_create_v1(token , u_ids):
    '''
    Creates a dm based on input and returns a unique dm id
    '''
    '''
    store = data_store.get()

    # Check valid token
    try:
        user_token = decode_jwt(token)
    except:
        raise AccessError('Could not decode token')

    check_valid_token(user_token)

    # Check for valid users
    check_valid_u_id_list()

    # Generate new dm_id
    dm_id = generate_dm_id()

    # Generate dm_names
    dm_names = generate_dm_names(u_ids, store)

    store['dm'].append({
        'dm_id': dm_id,
        'owner_id': user_token['u_id'],
        'users': dm_names,
    })

    data_store.set(store)
    
    return {
        'dm_id': dm_id
    }
    '''