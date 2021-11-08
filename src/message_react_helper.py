from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
from src.error import InputError

def check_if_message_already_reacted_to(message, u_id): 
    for react in message['reacts']: 
        if u_id in react['u_ids']: 
            raise InputError(description="You already reacted to this message")
    return

def check_user_in_channel(channel, u_id_given): 
    for member in channel['all_members']: 
        if member['u_id'] == u_id_given: 
            return 
    raise InputError(description="You are not a member of this channel")

def check_user_in_dm(dm, u_id_given): 
    for member in dm['members']: 
        if member == u_id_given: 
            return 
    raise InputError(description="You are not a member of this dm")

def check_react_id_is_valid(react_id, message): 
    for react in message['reacts']: 
        if react_id == react['react_id']:
            return
    raise InputError(description="react_id does not exit in streams")

def react_dm_message(u_id, react_id, message, dm):
    store = open_pickle()
    
    check_user_in_dm(dm, u_id)
    check_react_id_is_valid(react_id, message)
    check_if_message_already_reacted_to(message, u_id)

    for dm_store in store['dm']:
        for message_store in dm_store['messages']:
            if message_store['message_id'] == message['message_id']:
                for react in message_store['reacts']:
                    if react['react_id'] == react_id: 
                        react['u_ids'].append(u_id)
                        react['is_this_user_reacted'] = True

    data_store.set(store)
    save_pickle()
    return

def react_channel_message (u_id, react_id, message, channel):
    store = open_pickle()

    check_user_in_channel(channel, u_id)
    check_react_id_is_valid(react_id, message)
    check_if_message_already_reacted_to(message, u_id)

    for channel_store in store['channels']:
        for message_store in channel_store['messages']:
            if message_store['message_id'] == message['message_id']:
                for react in message_store['reacts']:
                    if react['react_id'] == react_id: 
                        react['u_ids'].append(u_id)
                        react['is_this_user_reacted'] = True

    data_store.set(store)
    save_pickle()
    return