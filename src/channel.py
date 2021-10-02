from src.error import InputError, AccessError
from src.data_store import data_store
from src.channel_details_helper import check_authorised_user, check_channel_id, get_user_details
from src.channels_create_helper import check_auth_id_exists
from src.channel_join_helper import find_user, find_channel, check_authorised_member

def channel_invite_v1(auth_user_id, channel_id, u_id):
    return {
    }

def channel_details_v1(auth_user_id, channel_id):
    store = data_store.get()

    #check valid u_id
    check_auth_id_exists(auth_user_id, store)
    #check channel_id exists
    check_channel_id(channel_id, store)
    #check user is part of given channel_id 
    check_authorised_user(auth_user_id, channel_id, store)

    #loop through channel list and find given channel_id
    channel_dictionary = {}
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            #loop through owner list and add dictionaries to a list
            owner_list = []
            for owner in channel['owner_members']:
                #get user details for owner
                owner_dictionary = get_user_details(owner['u_id'], store)                
                owner_list.append(owner_dictionary)

            #loop through member list and add dictionaries to a list
            members_list = []
            for member in channel['all_members']:
                #get user details for member
                member_dictionary = get_user_details(member['u_id'], store)
                members_list.append(member_dictionary)
            
            #add all entries to channel_dictionary
            channel_dictionary = {
                'name': channel['name'],
                'is_public': channel['is_public'],
                #add list containing dictionaries of owner_members
                'owner_members': owner_list,
                #add list containing dictionaries of members
                'all_members': members_list,
            }

    return channel_dictionary


def channel_messages_v1(auth_user_id, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_join_v1(auth_user_id, channel_id):
    store = data_store.get()
    
    # Check if channel_id valid 
    check_channel_id(channel_id, store)
    
    # Check if user is already member of channel
    check_authorised_member(auth_user_id, channel_id, store)
    
    # Checks if user exists and if so stores location in list
    user_join = find_user(auth_user_id, store)
    
    # Stores location of channel in list
    channel_join = find_channel(channel_id, store)
    
    # If channel is private and user is not global owner
    # prevent user from joining 
    if channel_join['is_public'] == False and user_join['is_streams_owner'] == False:
        raise AccessError
    
    # Create member dictionary  
    member_dictionary = {
        "u_id": user_join['u_id']
    }
    
    # Append user id to member list
    channel_join['all_members'].append(member_dictionary)
    
    data_store.set(store)
    return {}
