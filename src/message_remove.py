from src.data_store import data_store
from src.token_helper import decode_jwt, check_valid_token
from src.message_id_generator import message_id_generate
from src.data_store import data_store
from src.channel_details_helper import check_authorised_user
from datetime import datetime
from src.channel_messages_helper import get_channel, check_message_is_right_character_length
from src.dm_helper import check_dm_id_exists, check_user_in_dm
from src.channels import channels_list_v1
from src.dm_list import dm_list_v1
 

def message_remove_v1(u_id, message_id): 
    # store = data_store.get()        # channels = channels_list_v1(u_id)
    
    # dms = dm_list_v1(u_id)

    # if message_id in dms['messages']['message_id']:
    #     del dm['messages']

    
    # # for dm in dms: 
    # #     if dm['messages']['u_id'] == u_id or dm['owner_id'] == u_id:
    # #         if message_id == dm['messages']['message_id']: 
    # #             dm['messages'].remove(message)
            
    # data_store.set(store)

    return {}