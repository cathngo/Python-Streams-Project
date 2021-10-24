from src.data_store import data_store
from src.channels_create_helper import check_valid_name
from src.data_persistence import save_pickle, open_pickle

'''
Make a list with all the channels that the given auth_user_id is part of 

Arguments:
    auth_user_id (int) - user's id that is created when they first register into Streams

Exceptions:
InputError - Occurs when:
    - auth_user_id is invalid

Return Value:
    returns a list of dictionaries with the keys 'channel_id' and 'name' of the channels
    that auth_user_id is part of
'''
def channels_list_v1(auth_user_id):
    store = open_pickle()
    
    joined_channels = []
    
    #check all the channels in the database
    for channel in store['channels']:
        
        #loop through all the members of each channel
        for directoy_user_id in channel['all_members']:
            if directoy_user_id['u_id'] == auth_user_id:
                temp_dict = {
            		'channel_id': channel['channel_id'],
            		'name': channel['name'],
        		}
                joined_channels.append(temp_dict)
    
    return {
        'channels': joined_channels
    }
'''
Make a list with all the channels in the database 

Arguments:
    auth_user_id (int) - user's id that is created when they first register into Streams

Exceptions:
InputError - Occurs when:
    - auth_user_id is invalid

Return Value:
    returns a list of dictionaries with the keys 'channel_id' and 'name'
'''
def channels_listall_v1(auth_user_id):
    store = open_pickle()
    
    all_channels = []
    
    #check all the channels in the database
    for channel in store['channels']:
    
        temp_dict = {
    		'channel_id': channel['channel_id'],
    		'name': channel['name'],
		}
        all_channels.append(temp_dict)
    
    return {
        'channels': all_channels  
    }
    
'''
Creates a new channel for a user and stores it in the datastore

Arguments:
    auth_user_id (int) - user's id that is created when they first register into Streams
    name (string) - name of the channel
    is_public (boolean) - determines whether a channel is private (false) or public (true)

Exceptions:
InputError - Occurs when:
    - The length of name is less than 1 or more than 20 characters

Return Value:
    returns a dictionary containing a unique channel_id if the channel is successfully created
'''
def channels_create_v1(auth_user_id, name, is_public):


    store = open_pickle()

    check_valid_name(name)
    
    #create channel_id
    channel_id = len(store['channels'])

    #store details
    store['channels'].append (
        {
            'channel_id': channel_id,
            'name': name,
            'is_public': is_public,
            'owner_members': [
                {            
                    'u_id': auth_user_id,   
                }
            ],
            'all_members': [
                {          
                    'u_id': auth_user_id,
                }
            ],      
            'messages': [],                  
        }
    )
    
    data_store.set(store)
    save_pickle()
    
    return {
        'channel_id': channel_id           
    }   
