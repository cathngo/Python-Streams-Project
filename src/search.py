from src.data_persistence import open_pickle
from src.error import InputError
from src.search_helper import messages_in_channel, messages_in_dms

def find_message(u_id: int, query: str):
    '''
    Given a query string, return a collection of messages 
    in all of the channels/DMs that the user has joined that contain the query.

    Arguments:
        u_id (int) - id of the user sending 
        query_str (string) - the query_str that we need to find in messages

    Exceptions:
        InputError when:
      
        length of query_str is less than 1 or over 1000 characters

    Return Value: 
        A list with the messages found.

    '''
    store = open_pickle()
    from_ch = messages_in_channel(u_id, query, store['channels'])
    from_dms = messages_in_dms(u_id, query, store['dm'])
    return {'messages': from_ch + from_dms}