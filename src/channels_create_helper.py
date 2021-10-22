from src.error import InputError, AccessError

#check name is less than 1 or greater than 20 characters
def check_valid_name(name):
    if len(name) < 1 or len(name) > 20:
        raise InputError("Invalid channel name: name must be < 1 or > 20 characters")


#check auth_id exists
def check_auth_id_exists(auth_user_id, store):
    pass