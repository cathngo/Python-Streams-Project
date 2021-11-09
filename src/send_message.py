from src.data_store import data_store
from src.message_id_generator import message_id_generate
from src.data_store import data_store
from src.channel_details_helper import check_authorised_user
from datetime import datetime
from src.channel_messages_helper import get_channel, check_message_is_right_character_length
from src.dm_helper import check_dm_id_exists, check_user_in_dm
from src.data_persistence import save_pickle, open_pickle
from src.user_stats_helper import update_messages_sent
from src.users_stats_helper import update_messages_exist


def message_send_channel(u_id, channel_id, message):
    '''
Send a message from the authorised user to the channel specified by channel_id.

Arguments:
    u_id (int) - the id of the authorised user that is sending the channel
    channel_id (int) - the id of the channel that the user is sending the message to
    message (string) - the message the authorised user wishes to send to the specified channel

Exceptions:
    InputError - Occurs when any of:
        -channel_id does not refer to a valid channel
        -length of message is less than 1 or over 1000 characters
    AccessError - Occurs when:
        -channel is valid and the authorised user is not a member of the channel
Return Value: 
    Returns a messaged_id of type int when the message is sent in the channel
'''
    store = open_pickle()
    
    channel = get_channel(channel_id, store)
    check_authorised_user(u_id, channel_id, store)
    
    message_length = len(message)  
    check_message_is_right_character_length(message_length)
    
    message_id = message_id_generate()
    
    time_created = int(datetime.now().timestamp())
    
    channel['messages'].append(
        {
        'message_id': message_id, 
        'u_id': u_id, 
        'message': message,
        'time_created': time_created,    
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
        }
    )

    #increment user's stats count for messsages_sent by one
    update_messages_sent(u_id, store, 1)
    #increment number of existing msgs in workspace stats by one
    update_messages_exist(store, 1)

    data_store.set(store)
    save_pickle()
    return {
        'message_id': message_id
    }
'''
Send a message from the authorised user to the dm specified by dm_id.

Arguments:
    u_id (int) - the id of the authorised user that is sending the dm
    dm_id (int) - the id of the dm that the user is sending the message to
    message (string) - the message the authorised user wishes to send to the specified dm

Exceptions:
    InputError - Occurs when any of:
        -dm_id does not refer to a valid dm
        -length of message is less than 1 or over 1000 characters
    AccessError - Occurs when:
        -dm is valid and the authorised user is not a member of the dm
Return Value: 
    Returns a messaged_id of type int when the message is sent in the dm
'''
def message_send_dm(u_id, dm_id, message):
    store = open_pickle()
    
    dm = check_dm_id_exists(dm_id, store)
    check_user_in_dm(u_id, dm)
    
    message_length = len(message)  
    check_message_is_right_character_length(message_length)
    
    message_id = message_id_generate()
    
    time_created = int(datetime.now().timestamp())
    
    dm['messages'].append(
        {
        'message_id': message_id, 
        'u_id': u_id, 
        'message': message,
        'time_created': time_created,    
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
        }
    )
    #increment user's stats count for messsages_sent by one
    update_messages_sent(u_id, store, 1)
    #increment number of existing msgs in workspace stats by one
    update_messages_exist(store, 1)

    
    data_store.set(store)
    save_pickle()


    return {
        'message_id': message_id
    }
