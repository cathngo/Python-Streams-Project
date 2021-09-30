from src.data_store import data_store
from src.auth import auth_register_v1
from src.channels_create_helper import check_valid_name, check_auth_id_exists
from src.auth import auth_register_v1

def channels_list_v1(auth_user_id):
    store = data_store.get()
    check_auth_id_exists(auth_user_id, store)
    
    joined_channels = []
    
    #check all the channels in the database
    for channel in store['channels']:
        #prevent from adding private channels
        if channel['is_public'] == False : continue
        
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
    store = data_store.get()
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
    
def channels_create_v1(auth_user_id, name, is_public):
    store = data_store.get()

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
        }
    )
    
    data_store.set(store)
    
    return {
        'channel_id': channel_id           
    }   
