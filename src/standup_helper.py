from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
from src.error import InputError
from src.channel_join_helper import find_channel
from src.message_id_generator import message_id_generate
from datetime import datetime

def check_standup_length(length):
    if length < 0:
        raise InputError(description='length is a negative integer')

def finish_standup(u_id, channel_id):
    '''
    Once standups are finished, all of the messages sent to standup/send are packaged together
    in one single message posted by the user who started the standup and sent as a message to
    the channel the standup was started in, timestamped at the moment the standup finished
    '''
    store = open_pickle()

    channel = find_channel(channel_id, store)

    standup_message = ''
    for msg in channel['standup']['messages']:
        standup_message += (msg['handle'] + ': ' + msg['message'] + '\n')

    standup_message_id = message_id_generate()
    time_created = int(datetime.now().timestamp())

    channel['messages'].append(
        {
        'message_id': standup_message_id, 
        'u_id': u_id, 
        'message': standup_message,
        'time_created': time_created,
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

def check_standup_message_length(message):
    if len(message) > 1000:
        raise InputError(description='length of message cannot be over 1000 characters')