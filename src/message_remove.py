from src.data_store import data_store
from src.error import AccessError, InputError
from src.data_persistence import save_pickle, open_pickle

#input error is message_id was not found

'''
Given a message_id for a message, this message is removed from the channel/DM

Arguments:
    u_id (int) - the id of the authorised user that is sending the channel
    message_id (int) - the id of the channel that the user is deleting

Exceptions:
    InputError - Occurs when any of:
        -message_id does not refer to a valid message within a channel/DM that the authorised user has joined
    AccessError - Occurs when:
    when message_id refers to a valid message in a joined channel/DM and none of the following are true:    
        -the message was sent by the authorised user making this request
        -the authorised user has owner permissions in the channel/DM
Return Value: 
    Returns an empty dictionary if the message is successfully removed
'''

def message_remove_v1(u_id, message_id): 
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
        raise AccessError(description="Cannot delete message because you do not have the needed permissions")

    if message_id_exists_channel == False and message_id_exists_dm == False: 
        raise InputError(description="Message id was not found in channels or dms")
    
    for channel in store['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id and (message['u_id'] == u_id or owner_channel == True):
                channel['messages'].remove(message)
    
    for dm in store['dm']:
        for message in dm['messages']:
            if message['message_id'] == message_id and (message['u_id'] == u_id or owner_dm == True):
                dm['messages'].remove(message)    

    data_store.set(store)
    save_pickle()

    return {}