from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
from src.token_helper import decode_jwt, check_valid_token
from src.error import InputError, AccessError
from src.standup_helper import check_standup_message_length
from src.channel_details_helper import check_authorised_user
from src.dm_helper import check_user_in_dm
from src.channel_join_helper import find_channel
from src.message_id_generator import message_id_generate
from datetime import datetime

'''
Helper functions
'''
def check_valid_channel_id(channel_id):
    '''
    Checks if the given channel id exists in the database
    '''
    store = open_pickle()
    channel_exists = False

    for channel in store['channel']:
        if channel['channel_id'] == channel_id:
            channel_exists = True
    
    return channel_exists

def check_valid_dm_id(dm_id):
    '''
    Checks if the given dm id exists in the database
    '''
    store = open_pickle()
    dm_exists = False

    for dm in store['dm']:
        if dm['dm_id'] == dm_id:
            dm_exists = True

    return dm_exists

def find_user_channels(u_id):
    '''
    Returns a list of the channels the user has joined
    '''
    store = open_pickle()
    user_channels = []

    for channel in store['channels']:
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                user_channels.append(channel)

    return user_channels

def find_user_dms(u_id):
    '''
    Returns a list of the dms the user has joined
    '''
    store = open_pickle()
    user_dms = []

    for dm in store['dm']:
        for member_id in dm['members']:
            if member_id == u_id:
                user_dms.append(dm)

    return user_dms

def find_og_message_id(og_message_id, u_id):
    '''
    Checks if og_message_id refers to a valid message within a channel/DM that the authorised user has joined
    '''
    user_channels = find_user_channels(u_id)
    user_dms = find_user_dms(u_id)

    for channel in user_channels:
        for message in channel['messages']:
            if message['message_id'] == og_message_id:
                return message
                
    for dm in user_dms:
        for message in dm['messages']:
            if message['message_id'] == og_message_id:
                return message

    raise InputError(description='og_message_id does not refer to a valid message within a channel/DM that the authorised user has joined')



def message_share(token, og_message_id, message, channel_id, dm_id):
    '''
    Share an existing message across channels and dms

    Arguments:
        token (string) - user's token
        og_message_id (int) - id of message being shared
        message (string) - optional message in addition to the shared message, will be an empty string if no message is given
        channel_id (int) - channel that the message is being shared to, and is -1 if it is being sent to a DM
        dm_id (int) - DM that the message is being shared to, and is -1 if it is being sent to a channel

    Exceptions:
        InputError - Occurs when any of:
            - both channel_id and dm_id are invalid
            - neither channel_id nor dm_id are -1
            - og_message_id does not refer to a valid message within a channel/DM that the authorised user has joined
            - length of message is more than 1000 characters
        
        AccessError - Occurs when any of:
            - Invalid token
            - the pair of channel_id and dm_id are valid (i.e. one is -1, the other is valid) and the authorised user
            has not joined the channel or DM they are trying to share the message to

    Return Value:
        Returns a dictionary containing 'shared_message_id' - an integer representing the message id for the new message
    '''
    store = open_pickle()

    # Check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    # Error checks
    if check_valid_channel_id(channel_id) is False and check_valid_dm_id(dm_id) is False:
        raise InputError(description='both channel_id and dm_id are invalid')

    if channel_id != -1 and dm_id != -1:
        raise InputError(description='neither channel_id nor dm_id are -1')

    # Check if user has joined the channel/DM being shared to
    if dm_id == -1:
        check_authorised_user(user_token['u_id'], channel_id, store)
    else:
        for dm_iter in store['dm']:
            if dm_iter['dm_id'] == dm_id:
                check_user_in_dm(user_token['u_id'], dm_iter)

    og_message = find_og_message_id(og_message_id, user_token['u_id'])

    check_standup_message_length(message)

    # Create new message to be shared
    shared_message_id = message_id_generate()
    new_shared_message = og_message['message'] + ' ' + message
    time_created = int(datetime.now().timestamp())

    new_message = {
        'message_id': shared_message_id, 
        'u_id': user_token['u_id'], 
        'message': new_shared_message,
        'time_created': time_created,
    }

    # Share og message into channel/DM    
    if dm_id == -1:
        channel_share = find_channel(channel_id, store)
        channel_share['messages'].append(new_message)
    else:
        for dm_iter in store['dm']:
            if dm_iter['dm_id'] == dm_id:
                dm_iter['messages'].append(new_message)

    data_store.set(store)
    save_pickle()

    return {
        'shared_message_id': shared_message_id,
    }