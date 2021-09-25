from src.data_store import data_store
from src.auth import auth_register_v1
from src.channels_create_helper import check_valid_name, check_auth_id_exists

def channels_list_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall_v1(auth_user_id):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create_v1(auth_user_id, name, is_public):
    store = data_store.get()

    check_valid_name(name)
    check_auth_id_exists(auth_user_id, store)
    
    #create channel id
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