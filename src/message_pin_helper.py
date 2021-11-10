from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
from src.error import InputError, AccessError
from src.remove_edit_message_helper import check_channel_owner, check_is_streams_owner
from src.message_react_helper import check_user_in_channel, check_user_in_dm

def check_channel_message_permissions_message_pin(u_id, channel): 
    is_streams_owner = check_is_streams_owner(u_id)
    is_channel_owner = check_channel_owner(u_id, channel)

    if (is_streams_owner == False and is_channel_owner == False): 
        raise AccessError(description="Cannot pin message because you do not have the needed permissions in the channel")

def check_dm_owner_message_pin(u_id, dm):
    if dm['owner_id'] == u_id:
        return
    raise AccessError(description="You do not have dm owner permissions in this dm")

def check_if_message_already_pinned(message):
    if message['is_pinned'] == True:
        raise InputError(description= "Message is already pinned")

def check_if_message_already_unpinned(message):
    if message['is_pinned'] == False:
        raise InputError(description= "Message is already unpinned")

def pin_channel_message(u_id, message_id, message, channel):
    store = open_pickle()
    
    check_if_message_already_pinned(message)
    check_user_in_channel(channel, u_id)
    check_channel_message_permissions_message_pin(u_id, channel)
    
    for channel_store in store['channels']:
        for message_store in channel_store['messages']:
            if message_store['message_id'] == message_id:
                message_store['is_pinned'] = True

    data_store.set(store)
    save_pickle()
    return

def pin_dm_message(u_id, message_id, message, dm):
    store = open_pickle()
    
    check_if_message_already_pinned(message)
    check_user_in_dm(dm, u_id)
    check_dm_owner_message_pin(u_id, dm)
    
    for dm_store in store['dm']:
        for message_store in dm_store['messages']:
            if message_store['message_id'] == message_id:
                message_store['is_pinned'] = True 

    data_store.set(store)
    save_pickle()
    return

def unpin_channel_message(u_id, message_id, message, channel):
    store = open_pickle()
    
    check_user_in_channel(channel, u_id)
    check_channel_message_permissions_message_pin(u_id, channel)
    check_if_message_already_unpinned(message)
    
    for channel_store in store['channels']:
        for message_store in channel_store['messages']:
            if message_store['message_id'] == message_id:
                message_store['is_pinned'] = False

    data_store.set(store)
    save_pickle()
    return

def unpin_dm_message(u_id, message_id, message, dm):
    store = open_pickle()
    
    check_user_in_dm(dm, u_id)
    check_dm_owner_message_pin(u_id, dm)
    check_if_message_already_unpinned(message)
    
    for dm_store in store['dm']:
        for message_store in dm_store['messages']:
            if message_store['message_id'] == message_id:
                message_store['is_pinned'] = False 

    data_store.set(store)
    save_pickle()
    return