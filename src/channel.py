from src.error import InputError, AccessError
from src.data_store import data_store
from src.channel_details_helper import check_authorised_user, check_channel_id, get_user_details
from src.channels_create_helper import check_auth_id_exists
from src.channels_invite_helper import check_u_id_exists
from src.channel_join_helper import find_user, find_channel, check_authorised_member
from src.channel_messages_helper import get_channel

def channel_invite_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()

    #check valid u_id
    check_u_id_exists(u_id, store)
    #check channel_id exists
    check_channel_id(channel_id, store)
    #check inviter is part of given channel_id
    check_authorised_user(auth_user_id, channel_id, store)
    
    #check u_id is already part of the given channel_id
    for channel in store['channels']:
        if channel['channel_id'] == channel_id: 
            #check u_id is already part of the channel
            for dict in channel['all_members']:
                if dict['u_id'] == u_id:
                    raise InputError
            #if u_id is not part of the channel then append as a dictionary
            else:
                channel['all_members'].append({'u_id': u_id})
            #break to prevent having to checking other channels
            break
    
    data_store.set(store)
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

#the caller must decrease messages['message_id'] by 50 everytime it called until it is < 50, otherwise this funciton will not work. 
def channel_messages_v1(auth_user_id, channel_id, start):
    store = data_store.get()
    
    #check valid u_id
    check_auth_id_exists(auth_user_id, store)
    #check channel_id exists
    channel = get_channel(channel_id, store)
    #check user is part of given channel_id 
    check_authorised_user(auth_user_id, channel_id, store)
    

    #gets the current lenth of the messages
    message_id = len(channel['messages'])    
    
    #checks that the number of messages has not been over counted or
    #if start is greater than the number of messages in the page
    if start < 0 or start > message_id:
        raise AccessError
 
    #checks that the last page is not reached otherwise it continues 
    #that there will be another page to come by not making end = -1.      
    if message_id - start < 50:
        page_length = message_id
        end = -1
    else:
        page_length = 50 + start
        end = page_length
    
    max_message_id = message_id - 1
   
    #goes through the messages in a 0 - 50, 50 - 100, 100 - 150, in pagination 
    #manner, always starting from the first index and then continuing on the 
    #following call
    message_list = []
    for i in range(start, page_length):
        message_list.append(channel['messages'][max_message_id - i])  
    
    #returning a single dictionary with a key that is a list.  
    return {
        'messages': message_list, 
        'start': start,
        'end': end,
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
