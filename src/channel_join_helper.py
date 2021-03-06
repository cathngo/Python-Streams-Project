from src.error import InputError
def find_user(auth_user_id, store):
    temp_user = {}
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            temp_user = user
    return temp_user

def find_channel(channel_id, store):
    temp_channel = {}
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            temp_channel = channel
    return temp_channel

def check_authorised_member(auth_user_id, channel_id, store):
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['u_id'] == auth_user_id:
                    raise InputError(description='not an authorised member')
    return