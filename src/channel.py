from src.error import InputError, AccessError
from src.data_store import data_store
from src.channel_details_helper import check_authorised_user, check_channel_id
from src.channels_create_helper import check_auth_id_exists

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
                owner_dictionary = {
                    'u_id': owner['u_id'],                   
                }                  
                owner_list.append(owner_dictionary)

            #loop through member list and add dictionaries to a list
            members_list = []
            for member in channel['all_members']:
                member_dictionary = {
                    'u_id': member['u_id'],                        
                }
                members_list.append(member_dictionary)
            
            #add all entries to channel_dictionary
            channel_dictionary = {
                'name' : channel['name'],
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
    return {
    }
