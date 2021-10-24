from src.data_store import data_store
from src.error import AccessError, InputError
from src.data_persistence import save_pickle, open_pickle



def message_edit_v1(u_id, message_id, message_given): 
    store = open_pickle() 
    owner_channel = False       
    for channel in store['channels']: 
        for owner in channel['owner_members']: 
            if owner['u_id'] == u_id: 
                owner_channel = True

    owner_dm = False
    for owner in store['dm']: 
        if owner['owner_id'] == u_id:
            owner_dm = True 
   
    #access error for not owner or did not send message for dm/channel
    user_sent_channel = False 
    for channel in store['channels']:
        for message in channel['messages']:
            if message['u_id'] == u_id:
                user_sent_channel = True
    
    user_sent_dm = False
    for dm in store['dm']:
        for message in dm['messages']:
            if message['u_id'] == u_id:
                user_sent_dm = True

    #check that the message_id exists
    message_id_exists_channel = False 
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                message_id_exists_channel = True
    
    message_id_exists_dm = False
    for dm in store['dm']:
        for message in dm['messages']:
            if message['message_id'] == message_id:
                message_id_exists_dm = True
    
    if (owner_dm == False and user_sent_dm == False) and (owner_channel == False and user_sent_channel == False):
        raise AccessError(description="Cannot edit message because you do not have the needed permissions")

    if message_id_exists_channel == False and message_id_exists_dm == False: 
        raise InputError(description="Message id was not found in channels or dms")
    
    #edit implementation
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id and (message['u_id'] == u_id or owner_channel == True):
                if message_given != '':
                    message['message'] = message_given 
                else: 
                    channel['messages'].remove(message)
    
    for dm in store['dm']:
        for message in dm['messages']:
            if message['message_id'] == message_id and (message['u_id'] == u_id or owner_dm == True):
                if message_given != '':
                    message['message'] = message_given 
                else: 
                    dm['messages'].remove(message)

    data_store.set(store)
    save_pickle()
    return {}