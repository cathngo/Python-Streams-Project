from src.data_store import data_store
from src.token_helper import decode_jwt, check_valid_token
from src.message_id_generator import message_id_generate
from src.data_store import data_store
from src.channel_details_helper import check_authorised_user
from datetime import datetime
from src.channel_messages_helper import get_channel, check_message_is_right_character_length
from src.dm_helper import check_dm_id_exists, check_user_in_dm
 
def message_send_channel(u_id, channel_id, message):
    store = data_store.get()
    
    channel = get_channel(channel_id, store)
    check_authorised_user(u_id, channel_id, store)
    
    message_length = len(message)  
    check_message_is_right_character_length(message_length)
    
    message_id = message_id_generate()
    
    time_created = float(datetime.utcnow().timestamp())
    
    channel['messages'].append(
        {
        'message_id': message_id,
        'u_id': u_id, 
        'message': message,
        'time_created': time_created,    
        }
    )

    return {
        'message_id': message_id
    }

def message_send_dm(u_id, dm_id, message):
    store = data_store.get()
    
    dm = check_dm_id_exists(dm_id, store)
    check_user_in_dm(u_id, dm)
    
    message_length = len(message)  
    check_message_is_right_character_length(message_length)
    
    message_id = message_id_generate()
    
    time_created = float(datetime.utcnow().timestamp())
    
    dm['messages'].append(
        {
        'message_id': message_id,
        'u_id': u_id, 
        'message': message,
        'time_created': time_created,    
        }
    )

    return {
        'message_id': message_id
    }