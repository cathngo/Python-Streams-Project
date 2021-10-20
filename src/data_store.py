'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

## YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [],
    'channels': [],
    'dm': [],
    'messages': [],
}
## YOU SHOULD MODIFY THIS OBJECT ABOVE

class Datastore:
    def __init__(self):
        self.__store = initial_object

    def get(self):
        return self.__store

    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store

print('Loading Datastore...')

global data_store
data_store = Datastore()

'''
Example of populated Datastore

data = {
    'users': [
        {
            'u_id': 0,
            'email': 'kanyewest@gmail.com',
            'password': 'hashedpw',
            'name_first': 'Kanye', 
            'name_last': 'West',
            'handle_str': 'kanyewest',
            'is_streams_owner': true,
            'session_list': [1001]
        },
        {
            'u_id': 1,
            'email': 'kanyesouth@gmail.com',
            'password': 'hashedpw',
            'name_first': 'Kanye', 
            'name_last': 'South',
            'handle_str': 'kanyesouth',
            'is_streams_owner': false,
            'session_list': [1002]
        },
    ],
    'channels': [
        {
            'channel_id': 0,
            'name': 'Haha',
            'is_public': true,
            'owner_members': [
                {            
                    'u_id': 0,   
                }
            ],
            'all_members': [
                {          
                    'u_id': 0,
                    'u_id': 1,
                }
            ],
            'messages': [],
        },
        {
            'channel_id': 1,
            'name': 'Yeeeezus',
            'is_public': true,
            'owner_members': [
                {            
                    'u_id': 1,   
                }
            ],
            'all_members': [
                {          
                    'u_id': 1,
                }
            ],
            'messages': [],
        },
    ]
}
'''