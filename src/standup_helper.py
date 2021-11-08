from src.error import InputError
from src.channel_join_helper import find_channel
from src.message_id_generator import message_id_generate
from datetime import datetime

def check_standup_length(length):
    if length < 0:
        raise InputError(description='length is a negative integer')

def finish_standup(u_id, channel_id, store):
    '''
    Once standups are finished, all of the messages sent to standup/send are packaged together
    in one single message posted by the user who started the standup and sent as a message to
    the channel the standup was started in, timestamped at the moment the standup finished
    '''
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
        }
    )

def check_standup_message_length(message):
    if len(message) > 1000:
        raise InputError(description='length of message cannot be over 1000 characters')