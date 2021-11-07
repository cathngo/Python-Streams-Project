from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
from src.token_helper import decode_jwt, check_valid_token
from src.channel_details_helper import check_channel_id, check_authorised_user
from src.channel_join_helper import find_channel
from src.standup_helper import check_standup_length, finish_standup
from datetime import datetime
from threading import Timer
from src.error import InputError

def standup_active(token, channel_id):
    '''
    For a given channel, return whether a standup is active in it, and what time the standup finishes

    Arguments:
        token (string) - user's token
        channel_id (int) - id of channel to start startup

    Exceptions:
        InputError - Occurs when:
            - channel_id does not refer to a valid channel
        
        AccessError - Occurs when any of:
            - Invalid token
            - channel_id is valid and the authorised user is not a member of the channel

    Return Value:
        Returns a dictionary containing 'is_active' - a boolean indivating whether there is
        already an active standup in the channel and 'time_finish' - an integer (unix timestamp)
        which indicates the end of the standup
    '''
    store = open_pickle()

    # Check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    # Error checks
    check_channel_id(channel_id, store)
    check_authorised_user(user_token['u_id'], channel_id, store)

    temp = find_channel(channel_id, store)

    time_current = int(datetime.now().timestamp())
    time_finish = temp['standup']['time_finish']

    is_active = True if time_current < time_finish else False

    if is_active is False:
        time_finish = None
        temp['standup'].clear()

    data_store.set(store)
    save_pickle()

    return {
        'is_active': is_active,
        'time_finish': time_finish,
    }

def standup_start(token, channel_id, length):
    '''
    Start a new standup

    Arguments:
        token (string) - user's token
        channel_id (int) - id of channel to start startup
        length (int) - number of seconds the standup occurs for

    Exceptions:
        InputError - Occurs when any of:
            - channel_id does not refer to a valid channel
            - length is a negative integer
            - an active standup is currently running in the channel
        
        AccessError - Occurs when any of:
            - Invalid token
            - channel_id is valid and the authorised user is not a member of the channel

    Return Value:
        Returns a dictionary containing 'time_finish' - an integer (unix timestamp) which
        indicates the end of the standup
    '''
    store = open_pickle()

    # Check valid token
    user_token = decode_jwt(token)
    check_valid_token(user_token)

    # Error checks
    check_channel_id(channel_id, store)
    check_authorised_user(user_token['u_id'], channel_id, store)
    check_standup_length(length)

    temp = find_channel(channel_id, store)

    if temp['standup'] != {}:
        check = standup_active(token, channel_id)
        if check['is_active'] is True:
            raise InputError(description='an active standup is currently running in the channel')

    time_current = int(datetime.now().timestamp())
    time_finish = time_current + length

    temp['standup'] = {
        'channel_id': channel_id,
        'messages': [],
        'time_finish': time_finish,
    }

    # End startup after 'length' seconds
    t = Timer(length, finish_standup, args=[user_token['u_id'], channel_id, store])
    t.start()

    data_store.set(store)
    save_pickle()
    
    return {
        'time_finish': time_finish
    }