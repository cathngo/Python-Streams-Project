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
    'all_user_stats': [],
    'workspace_stats': {},
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
            'session_list': [1001],
            'profile_img_url': http://localhost:33327/static/0.jpg
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
            'password_reset': 'MAGQaXcfVdOlxArMqXJz'
            'profile_img_url': http://localhost:33327/static/0.jpg
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
                },
                {          
                    'u_id': 1,
                },
            ],
            'messages': [
                {
                'message_id': 1,
                'u_id': 1, 
                'message': 'hello',
                'time_created': 1635077917,
                },
            ],
        },
        {
            'channel_id': 1,
            'name': 'Yeeeezus',
            'is_public': true,
            'owner_members': [
                {            
                    'u_id': 1,   
                },
            ],
            'all_members': [
                {          
                    'u_id': 1,
                },
            ],
            'messages': [],
        },
    ],
    'dm': [
        {
            'dm_id': 1,
            'name': 'kanyesouth, kanyewest',
            'owner_id': 0
            'members': [1,0],
            'messages': [
                {
                'message_id': 2,
                'u_id': 1, 
                'message': 'hello',
                'time_created': 1635077932,
                },
            ],
        },
        {
            'dm_id': 2,
            'name': 'kanyesouth',
            'owner_id': 1
            'members': [1],
            'messages': [
                {
                'message_id': 3,
                'u_id': 1, 
                'message': 'hello',
                'time_created': 1635077952,
                },
            ],
        },
    ],
    'all_user_stats': [
        {
            'u_id': 0,
            'user_stats': {
                'channels_joined': [{'num_channels_joined': 0, 'time_stamp': 1635077932},{'num_channels_joined': 1, 'time_stamp': 1635077932}],
                'dms_joined': [{'num_dms_joined': 0, 'time_stamp': 1635077932},{'num_dms_joined': 1, 'time_stamp': 1635077932}],
                'messages_sent': [{'num_messages_sent': 0, 'time_stamp': 1635077932},{'num_messages_sent': 1, 'time_stamp': 1635077932}],
                'involvement_rate':1.2,          
            },
        },
        {
            'u_id': 1,
            'user_stats': {
                'channels_joined': [{'num_channels_joined': 0, 'time_stamp': 1635077932},{'num_channels_joined': 1, 'time_stamp': 1635077932}],
                'dms_joined': [{'num_dms_joined': 0, 'time_stamp': 1635077932},{'num_dms_joined': 1, 'time_stamp': 1635077932}],
                'messages_sent': [{'num_messages_sent': 0, 'time_stamp': 1635077932},{'num_messages_sent': 1, 'time_stamp': 1635077932}],
                'involvement_rate': 1.3,          
            },
        },
    ],

    'workspace_stats': {
        'channels_exist': [{'num_channels_exist': 0, 'time_stamp': 12},{'num_channels_exist': 1, 'time_stamp': 13}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': 12},{'num_dms_exist': 1, 'time_stamp': 13}],
        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': 12},{'num_messages_exist': 1, 'time_stamp': 13}],
        'utilization_rate': 16,    
    },
}
'''
