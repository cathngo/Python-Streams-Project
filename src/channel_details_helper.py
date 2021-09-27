from src.error import InputError, AccessError


def check_channel_id(channel_id, store):
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return 
    raise InputError

def check_authorised_user(auth_user_id, channel_id, store):
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            for owner in channel['owner_members']:
                if owner['u_id'] == auth_user_id:
                    return 
            for member in channel['all_members']:
                if member['u_id'] == auth_user_id:
                    return 
    raise AccessError