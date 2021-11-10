from src.data_store import data_store
from src.error import AccessError, InputError
from src.data_persistence import save_pickle, open_pickle
from src.remove_edit_message_helper import in_channel_search, in_dm_search, remove_channel_message, remove_dm_message
from src.users_stats_helper import update_messages_exist



def message_remove_v1(u_id, message_id):
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

    in_channel_found = in_channel_search(message_id)
    
    in_dm_found = in_dm_search(message_id)

    if in_channel_found:
        remove_channel_message(u_id, message_id, in_channel_found['message'], in_channel_found['channel'])
        return {}

    if in_dm_found:
        remove_dm_message(u_id, message_id, in_dm_found['message'], in_dm_found['dm'])
        return {}

    raise InputError(description= "message_id is not valid")

    

    
