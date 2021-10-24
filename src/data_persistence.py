import pickle
from src.data_store import data_store
from json import dumps, loads
from src.error import AccessError

def savep():
    store = data_store.get()

    with open('database.p', 'wb') as FILE:
        pickle.dump(store, FILE)

    

def openp():
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

def savej():
    store = data_store.get()
    with open('database.json', 'w') as FILE:
       FILE.write(dumps(store))
    

def openj():
    #need to change if no file so first time saving to databse dont raise accesserror but just do normal one?
    success = True
    store = data_store.get()
    try:
        with open('database.json', 'r') as FILE:
            store = loads(FILE.read())
    except:
        success = False
    if success == False:
        store = data_store.get()
    return store