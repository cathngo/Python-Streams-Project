from src.error import InputError, AccessError

#check u_id exists
def check_u_id_exists(auth_user_id, store):
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            break
    else:
        raise InputError
        

