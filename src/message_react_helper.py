from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
from src.error import InputError

def check_if_message_already_reacted_to(message, u_id_given): 
    for react in message['reacts']: 
        for u_id in react['u_ids']: 
            if u_id == u_id_given: 
                if react['is_this_user_reacted'] == True: 
                    raise InputError(description="you already reacted to this message")
    return

def check_react_id_is_valid(react_id, message): 
    for react in message['reacts']: 
        if react_id == react['react_id']:
            return
    raise InputError(description="react_id does not exit in streams")


def react_dm_message(u_id, react_id, message, dm):
    store = open_pickle()

    check_react_id_is_valid(react_id, message)
    check_if_message_already_reacted_to(message, u_id)
    
    react_members = []
    react_members.append(u_id)

    for dm_store in store['dm']:
        for message_store in dm_store['messages']:
            if message_store['message_id'] == message['message_id']:
                for react in message_store['reacts']:
                    if react['react_id'] == react_id: 
                        react['u_ids'] = react_members
                        react['is_this_user_reacted'] = True

    
    data_store.set(store)
    save_pickle()
    return

def react_channel_message (u_id, react_id, message, channel):
    store = open_pickle()

    check_react_id_is_valid(react_id, message)
    check_if_message_already_reacted_to(message, u_id)
    
    react_members = []
    react_members.append(u_id)

    for channel_store in store['channels']:
        for message_store in channel_store['messages']:
            if message_store['message_id'] == message['message_id']:
                for react in message_store['reacts']:
                    if react['react_id'] == react_id: 
                        react['u_ids'] = react_members
                        react['is_this_user_reacted'] = True

    data_store.set(store)
    save_pickle()
    return