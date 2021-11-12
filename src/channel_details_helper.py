from src.error import InputError, AccessError

def check_channel_id(channel_id, store):
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return 
    raise InputError(description='Invalid channel id - channel id not found')

def check_authorised_user(auth_user_id, channel_id, store):
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['u_id'] == auth_user_id:
                    return 
    raise AccessError(description='Invalid user - u_id not found')

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
                'notifications': user['notifications'],                  
                'profile_img_url': user['profile_img_url']    
            }

    return owner_dictionary 
