from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
from src.error import AccessError
from src.users_stats_helper import update_messages_exist

def check_channel_owner(u_id, channel):
    is_channel_owner = False
    for owner in channel['owner_members']: 
        if owner['u_id'] == u_id:
            is_channel_owner = True
    return is_channel_owner


def check_dm_owner(u_id, dm):
    is_dm_owner = False
    if dm['owner_id'] == u_id:
        is_dm_owner = True
    return is_dm_owner

def check_user_sent_message_channel_dm(message, u_id):
    is_message_in_channel_dm = False
    
    if message['u_id'] == u_id:
        is_message_in_channel_dm = True
    
    return is_message_in_channel_dm

def check_is_streams_owner(u_id):
    store = open_pickle()
    is_stream_owner = False
    for user in store['users']:
        if user['u_id'] == u_id and user['is_streams_owner'] == True: 
            is_stream_owner = True
    return is_stream_owner
    
def check_channel_message_permissions(u_id, message, channel): 
    is_streams_owner = check_is_streams_owner(u_id)
    user_sent_message = check_user_sent_message_channel_dm(message, u_id)
    is_channel_owner = check_channel_owner(u_id, channel)

    if (is_streams_owner == False and user_sent_message == False and is_channel_owner == False): 
        raise AccessError(description='Cannot delete/edit message because you do not have the needed permissions in the channel')
    
    return 

def check_dm_message_permissions(u_id, message, dm): 
    user_sent_message = check_user_sent_message_channel_dm(message, u_id)
    is_dm_owner = check_dm_owner(u_id, dm)
    
    if (user_sent_message == False and is_dm_owner == False): 
        raise AccessError(description='Cannot delete/edit message because you do not have the needed permissions in the dm')
    return

def remove_channel_message (u_id, message_id, message, channel):
    
    store = open_pickle()

    check_channel_message_permissions(u_id, message, channel)

    for channel_store in store['channels']:
        for message_store in channel_store['messages']:
            if message_store['message_id'] == message_id:
                channel_store['messages'].remove(message)
                #decrement workspace stats for existing messsages by one if removed
                update_messages_exist(store, -1)

    data_store.set(store)
    save_pickle()
    return

def remove_dm_message(u_id, message_id, message, dm):
    store = open_pickle()
    
    check_dm_message_permissions(u_id, message, dm)
    
    for dm_store in store['dm']:
        for message_store in dm_store['messages']:
            if message_store['message_id'] == message_id:
                dm_store['messages'].remove(message) 
                #decrement workspace stats for existing messsages by one if removed
                update_messages_exist(store, -1)
    data_store.set(store)
    save_pickle()
    return

def in_channel_search(message_id):
    store = open_pickle()

    temp_dic_channel = {}
    for channel_store in store['channels']:
        for message_store in channel_store['messages']:
            if message_store['message_id'] == message_id:
                temp_dic_channel['channel'] = channel_store
                temp_dic_channel['message'] = message_store                    

    return temp_dic_channel

def in_dm_search(message_id):
    store = open_pickle()

    temp_dic_dm = {}
    for dm_store in store['dm']:
        for message_store in dm_store['messages']:
            if message_store['message_id'] == message_id:
                temp_dic_dm['dm'] = dm_store
                temp_dic_dm['message'] = message_store
    
    return temp_dic_dm

def edit_dm_message(u_id, message_id, message, dm, message_given):
    store = open_pickle()
    
    check_dm_message_permissions(u_id, message, dm)
    
    for dm_store in store['dm']:
        for message_store in dm_store['messages']:
            if message_store['message_id'] == message_id:
                if message_given != '':
                    message_store['message'] = message_given 
                else: 
                    dm_store['messages'].remove(message)
    data_store.set(store)
    save_pickle()
    return

def edit_channel_message (u_id, message_id, message, channel, message_given):
    
    store = open_pickle()

    check_channel_message_permissions(u_id, message, channel)

    for channel_store in store['channels']:
        for message_store in channel_store['messages']:
            if message_store['message_id'] == message_id:
                if message_given != '':
                    message_store['message'] = message_given 
                else: 
                    channel_store['messages'].remove(message_store)
    data_store.set(store)
    save_pickle()
    return
