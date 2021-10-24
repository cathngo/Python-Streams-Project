from src.data_store import data_store
from src.auth import auth_register_v1
from src.channels_create_helper import check_valid_name, check_auth_id_exists
from src.auth import auth_register_v1
from src.data_persistence import save_pickle, open_pickle
def channels_list_v1(auth_user_id):
    store = open_pickle()
    check_auth_id_exists(auth_user_id, store)
    
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

def channels_listall_v1(auth_user_id):
    store = open_pickle()
    check_auth_id_exists(auth_user_id, store)
    
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
    check_auth_id_exists(auth_user_id, store)
    
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
