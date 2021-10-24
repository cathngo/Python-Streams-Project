from src.data_store import data_store
from src.token_helper import decode_jwt, check_valid_token
from src.message_id_generator import MESSAGE_ID, message_id_generate
from src.data_store import data_store
from src.channel_details_helper import check_authorised_user
from datetime import datetime
from src.channel_messages_helper import get_channel, check_message_is_right_character_length, messages_pagination
from src.dm_helper import check_dm_id_exists, check_user_in_dm
from src.channels import channels_list_v1
from src.dm_list import dm_list_v1
from src.error import AccessError, InputError

def message_edit_v1(u_id, message_id, message_given): 
    store = data_store.get()
    
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

    return {}