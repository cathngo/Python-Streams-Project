from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
from src.error import InputError, AccessError

def remove_from_streams(global_user_id, u_id):
    store = open_pickle()
    new_global_found = False
    global_found = False
    #count how many global owners there are this cannot, be zero at the end of this function
    owners_count = 0 
    for user in store['users']:
        if user['is_streams_owner'] == True:
            owners_count += 1
        if user['u_id'] == u_id: 
            new_global_found = True
        if user['u_id'] == global_user_id and user['is_streams_owner'] == True: 
            global_found = True 


    if not global_found:   
        raise AccessError(description='the authorised user is not a global owner')
    elif not new_global_found or (new_global_found == True and owners_count == 1):
        raise InputError(description='The given u_ is not valid')


    for user in store['users']:
        if user['u_id'] == u_id:
            user['name_first'] = 'Removed'
            user['name_last'] = 'user'
            user['handle_str'] = ''
            user['email'] = ''

    for channel in store['channels']: 
        #remove the id from the owner members list
        for owner in channel['owner_members']:
            if owner['u_id'] == u_id:
                channel['owner_members'].remove(owner)
        #remove the id from the owner members list
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                channel['all_members'].remove(member)
        #update the messages
        for message in channel['messages']:
            if message['u_id'] == u_id:
                message['message'] = 'Removed user'
    
        
    for dm in store['dm']:
        #if u_id is the channel owner chage it into -1
        if dm['owner_id'] == u_id:
            dm['owner_id'] = -1
        #remove u_id as a member
        for member in dm['members']:
            if member['u_id'] == u_id:
                dm['members'].remove(member)
        #update the messages
        for message in dm['messages']:
            if message['u_id'] == u_id:
                message['message'] = 'Removed user'








    data_store.set(store)
    save_pickle()

    return dumps({})