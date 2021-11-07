from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
from src.token_helper import decode_jwt, check_valid_token
from src.channel_details_helper import check_channel_id, check_authorised_user
from src.channel_join_helper import find_channel
from src.standup_helper import check_standup_length, finish_standup
from datetime import datetime
from threading import Timer

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
        
        AccessError - Occurs when:
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
    #check_active_standup(token, channel_id)

    time_current = int(datetime.now().timestamp())   
    time_finish = time_current + length

    temp = find_channel(channel_id, store)

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