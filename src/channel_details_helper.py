from src.error import InputError, AccessError

def check_channel_id(channel_id, store):
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return 
    raise InputError("Invalid channel id - channel id not found")

def check_authorised_user(auth_user_id, channel_id, store):
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['u_id'] == auth_user_id:
                    return 
    raise AccessError("Invalid user - u_id not found")

def get_user_details(auth_user_id, store):
    owner_dictionary = {}
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            #create dictionary containing user details
            owner_dictionary = {
                'u_id': user['u_id'],
                'email': user['email'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
                'handle_str': user['handle_str'],            
            }

    return owner_dictionary 

def check_authorised_user_invalid_channel(channel_id, auth_user_id, store):
    found_channel = False
    found_user = False
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            found_channel = True
            for member in channel['all_members']:
                if member['u_id'] == auth_user_id:
                    found_user = True
                    return 
    if found_channel == False and found_user == False:
        raise AccessError("Invalid user - u_id not found")
    if found_channel == True and found_usr == False:
        raise InputError("Invalid channel id - channel id not found")