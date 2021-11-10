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
    '''
    Adds the message to the start of the messages list within dm

    Arguments:
        u_id (int) - id of the user sending 
        dm_id (int) - id of the dm
        message_id (int) - id of the message being sent
        message (string) - the message that is being sent
        time_sent (int) - time that the message is set to be sent

    Return Value: None

    '''
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
    '''
    Send a message from the authorised user to the DM specified by dm_id automatically at a specified time in the future.

    Arguments:
        u_id (int) - id of the user sending 
        dm_id (int) - id of the dm
        message_id (int) - id of the message being sent
        message (string) - the message that is being sent
        time_sent (int) - time that the message is set to be sent

    Exceptions:
        - dm_id does not refer to a valid DM raise InputError
        - length of message is over 1000 characters raise InputError
        - time_sent is a time in the past raise InputError
        - dm_id is valid and the authorised user is not a member of the DM they are trying to post to raise AccessError

    Return Value: message_id
    '''
 
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
