from src.data_store import data_store
from src.error import InputError
from src.remove_edit_message_helper import in_channel_search, in_dm_search
from src.message_pin_helper import pin_dm_message, pin_channel_message, unpin_channel_message, unpin_dm_message

def message_pin_v1(u_id, message_id):
    '''
Given a message within a channel or DM, mark it as "pinned".

Arguments:
    u_id (int) - the id of the authorised user that is trying to pin the message
    message_id (int) - the id of the message that the user is trying to pin

Exceptions:
    InputError - Occurs when any of:
        -message_id is not a valid message within a channel or DM that the authorised user has joined
        -the message is already pinned
    AccessError - Occurs when any of :
        - An invalid token was passed to the route
        - message_id refers to a valid message in a joined channel/DM and 
        the authorised user does not have owner permissions in the channel/DM

Return Value: 
    Returns an empty dictionary if the message is successfully pinned
'''
    in_channel_found = in_channel_search(message_id)
    in_dm_found = in_dm_search(message_id)

    if in_channel_found:
        pin_channel_message(u_id, message_id, in_channel_found['message'], in_channel_found['channel'])
        return {}
    
    if in_dm_found:
        pin_dm_message(u_id, message_id, in_dm_found['message'], in_dm_found['dm'])
        return {}

    raise InputError(description= "message_id is not valid")

def message_unpin_v1(u_id, message_id):
    '''
Given a message within a channel or DM, remove its mark as pinned.

Arguments:
    u_id (int) - the id of the authorised user that is trying to unpin the message
    message_id (int) - the id of the message that the user is trying to unpin

Exceptions:
    InputError - Occurs when any of:
        -message_id is not already pinned
    AccessError - Occurs when any of :
        - An invalid token was passed to the route
        - message_id refers to a valid message in a joined channel/DM and 
        the authorised user does not have owner permissions in the channel/DM

Return Value: 
    Returns an empty dictionary if the message is successfully unpinned
'''
    in_channel_found = in_channel_search(message_id)
    in_dm_found = in_dm_search(message_id)

    if in_channel_found:
        unpin_channel_message(u_id, message_id, in_channel_found['message'], in_channel_found['channel'])
        return {}
    
    if in_dm_found:
        unpin_dm_message(u_id, message_id, in_dm_found['message'], in_dm_found['dm'])
        return {}

    raise InputError(description= "message_id is not valid")