from src.data_persistence import open_pickle
from src.error import InputError
from src.search_helper import messages_in_channel, messages_in_dms

def find_message(u_id: int, query: str):
    store = open_pickle()
    from_ch = messages_in_channel(u_id, query, store['channels'])
    from_dms = messages_in_dms(u_id, query, store['dm'])
    return {'messages': from_ch + from_dms}