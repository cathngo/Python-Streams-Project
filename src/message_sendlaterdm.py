import time 
import threading 
from src.data_store import data_store
from src.message_id_generator import message_id_generate
from src.data_store import data_store
from src.channel_details_helper import check_authorised_user
from datetime import datetime
from src.channel_messages_helper import get_channel, check_message_is_right_character_length
from src.dm_helper import check_dm_id_exists, check_user_in_dm
from src.data_persistence import save_pickle, open_pickle
from src.channel_messages_helper import check_message_time, find_time_delay
from src.dm_helper import check_valid_u_id_list, generate_dm_id, generate_dm_names

def message_sendlaterdm_v1(u_id, channel_id, dm_id, time_sent):
    store = open_pickle()
    
    channel = get_channel(channel_id, store)
    check_authorised_user(u_id, channel_id, store)

    # Check for valid users
    check_valid_u_id_list(u_ids, store)
    message_length = len(message)  
    check_message_is_right_character_length(message_length)

    check_message_time(time_sent)
    time_delay = find_time_delay(time_sent)

    
    store['dm'].append({
        'dm_id': dm_id,
        'name': dm_name,
        'owner_id': user_token['u_id'],
        'members': dm_members,
        'messages': [],
        'time_created': time_sent, 
    })

    data_store.set(store)
    save_pickle()

    #t = threading.Timer(time_delay, )

    data_store.set(store)
    save_pickle()
    return {
        'dm_id': dm_id
    }