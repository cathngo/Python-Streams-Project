import pickle
from src.data_store import data_store
from json import dumps, loads
from src.error import AccessError

def save_pickle():
    store = data_store.get()
    with open('database.p', 'wb') as FILE:
        pickle.dump(store, FILE)

def open_pickle():
    success = True
    try:
        store = data_store.get()
        with open('database.p', 'rb') as FILE:
            store = pickle.load(FILE)
            print(store)
    except:
        success = False
        if success == False:
            store = data_store.get()
    return store
