from src.data_store import data_store
from src.error import InputError
from src.remove_edit_message_helper import in_channel_search, in_dm_search
from src.message_react_helper import react_dm_message, react_channel_message, unreact_dm_message, unreact_channel_message

def message_react_v1(u_id, message_id, react_id):
    '''
Given a message within a channel or DM the authorised user is part of, add a "react" to that particular message.

Arguments:
    u_id (int) - the id of the authorised user that is reacting to the message
    message_id (int) - the id of the message that the user is reacting to
    react_id (int) - the type of reaction that the user is making to the message

Exceptions:
    InputError - Occurs when any of:
        -message_id is not a valid message within a channel or DM that the authorised user has joined
        -react_id is not a valid react ID
        -the message already contains a react with ID react_id from the authorised user
    AccessError - Occurs when:
        - An invalid token was passed to the route

Return Value: 
    Returns an empty dictionary if the message is successfully reacted to
'''
    in_channel_found = in_channel_search(message_id)
    in_dm_found = in_dm_search(message_id)

    if in_channel_found:
        react_channel_message(u_id, react_id, in_channel_found['message'], in_channel_found['channel'])
        return {}
    
    if  in_dm_found:
        react_dm_message(u_id, react_id, in_dm_found['message'], in_dm_found['dm'])
        return {}

    raise InputError(description= "message_id is not valid")
    
def message_unreact_v1(u_id, message_id, react_id):
    '''
Given a message within a channel or DM the authorised user is part of, remove a "react" to that particular message.

Arguments:
    u_id (int) - the id of the authorised user that is unreacting to the message
    message_id (int) - the id of the message that the user is unreacting to
    react_id (int) - the type of reaction that the user is making to the message

Exceptions:
    InputError - Occurs when any of:
        -message_id is not a valid message within a channel or DM that the authorised user has joined
        -react_id is not a valid react ID
        -the message does not contain a react with ID react_id from the authorised user
    AccessError - Occurs when:
        - An invalid token was passed to the route

Return Value: 
    Returns an empty dictionary if the message is successfully unreacted to
'''
    in_channel_found = in_channel_search(message_id)
    in_dm_found = in_dm_search(message_id)

    if in_channel_found:
        unreact_channel_message(u_id, react_id, in_channel_found['message'], in_channel_found['channel'])
        return {}
    
    if  in_dm_found:
        unreact_dm_message(u_id, react_id, in_dm_found['message'], in_dm_found['dm'])
        return {}

    raise InputError(description= "message_id is not valid")