from src.data_store import data_store
from src.error import AccessError, InputError
from src.data_persistence import save_pickle, open_pickle
from src.remove_edit_message_helper import in_channel_search, in_dm_search, edit_channel_message, edit_dm_message



def message_edit_v1(u_id, message_id, message_given):
    '''
Given a message, update its text with new text. If the new message is an empty string, the message is deleted.

Arguments:
    u_id (int) - the id of the authorised user that is sending the channel
    message_id (int) - the id of the channel that the user is deleting
    message_given(string) - the message that the user wants to replace the existing message with

Exceptions:
    InputError - Occurs when any of:
        -length of message is over 1000 characters
        -message_id does not refer to a valid message within a channel/DM that the authorised user has joined
    AccessError - Occurs when:
    when message_id refers to a valid message in a joined channel/DM and none of the following are true:    
        -the message was sent by the authorised user making this request
        -the authorised user has owner permissions in the channel/DM
Return Value: 
    Returns an empty dictionary if the message is successfully edited
''' 
    if len(message_given) > 1000: 
        raise InputError(description='Message is greater than one thousand characters')
    
    in_channel_found = in_channel_search(message_id)
    
    in_dm_found = in_dm_search(message_id)

    if in_channel_found != {}:
        edit_channel_message(u_id, message_id, in_channel_found['message'], in_channel_found['channel'], message_given)
        return {}

    if  in_dm_found != {}:
        edit_dm_message(u_id, message_id, in_dm_found['message'], in_dm_found['dm'], message_given)
        return {}

    raise InputError(description= "message_id is not valid")

