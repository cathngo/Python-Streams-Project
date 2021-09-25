from src.error import InputError, AccessError

#check name is less than 1 or greater than 20 characters
def check_valid_name(name):
    if len(name) < 1 or len(name) > 20:
        raise InputError


#check auth id exists
def check_auth_id_exists(auth_user_id, store):
    found = False
    #empty list
    if store['users'] == []:
        raise AccessError
    else:
        #search for u_id in users
        for user in store['users']:
            if user['u_id'] == auth_user_id:
                found = True
    if found == False:
        raise AccessError