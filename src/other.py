from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
def clear_v1():
    store = open_pickle()
    store['users'] = []
    store['channels'] = []
    store['dm'] = []
    store['all_user_stats'] = []
    store['workspace_stats'] = {}
    data_store.set(store)
    save_pickle()
