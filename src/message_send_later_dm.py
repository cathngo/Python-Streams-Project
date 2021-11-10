import time 
from threading import Timer
from src.data_store import data_store
from src.message_id_generator import message_id_generate
from src.data_store import data_store
from src.channel_details_helper import check_authorised_user
from datetime import datetime
from src.channel_messages_helper import get_channel, check_message_is_right_character_length
from src.dm_helper import check_dm_id_exists, check_user_in_dm
from src.data_persistence import save_pickle, open_pickle
from src.channel_messages_helper import check_message_time, find_time_delay
from src.dm_helper import check_dm_id_exists, check_user_in_dm, obtain_user_details


def send_dm_later(u_id, dm_id, message_id, message, time_sent):
    store = open_pickle()
    
    dm = check_dm_id_exists(dm_id, store)
    dm['messages'].append(
        {
        'message_id': message_id, 
        'u_id': u_id, 
        'message': message,
        'time_created': time_sent,
        'is_pinned': False,
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
        }
    )
    data_store.set(store)
    save_pickle()

def message_sendlaterdm_v1(u_id, dm_id, message, time_sent):
    store = open_pickle()
    
    dm = check_dm_id_exists(dm_id, store)
    check_user_in_dm(u_id, dm)
    
    message_length = len(message)  
    check_message_is_right_character_length(message_length)
    
    check_message_time(time_sent)
    time_delay = find_time_delay(time_sent)

    message_id = message_id_generate()
    
    thread1 = Timer(time_delay, send_dm_later, [u_id, dm_id, message_id, message, time_sent])
    thread1.start()

    data_store.set(store)
    save_pickle()

    return {
        'message_id': message_id
    }