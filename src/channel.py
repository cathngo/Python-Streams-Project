from src.error import InputError, AccessError
from src.data_store import data_store
from src.channel_details_helper import check_authorised_user, check_channel_id, get_user_details
from src.channels_create_helper import check_auth_id_exists
from src.channels_invite_helper import check_u_id_exists
from src.channel_join_helper import find_user, find_channel, check_authorised_member
from src.message_id_generator import message_id_generate
from src.channel_messages_helper import get_channel, messages_pagination
from src.dm_helper import check_dm_id_exists, check_user_in_dm

def channel_invite_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()

    #check valid auth_id
    check_auth_id_exists(auth_user_id, store)    
    #check channel_id exists
    check_channel_id(channel_id, store)
    #check inviter is part of given channel_id
    check_authorised_user(auth_user_id, channel_id, store)
    #check valid u_id
    check_u_id_exists(u_id, store)
    
    #check u_id is already part of the given channel_id
    for channel in store['channels']:
        if channel['channel_id'] == channel_id: 
            #check u_id is already part of the channel
            for dict in channel['all_members']:
                if dict['u_id'] == u_id:
                    raise InputError
            #if u_id is not part of the channel then append as a dictionary
            channel['all_members'].append({'u_id': u_id})
            #break to prevent having to checking other channels
            break
    
    data_store.set(store)
    return {
    }
    
'''
Provides basic details about the given channel that the authorised user is a member of

Arguments:
    auth_user_id (int) - user's id that is created when they first register into Streams
    channel_id (int) - channel id that is allocated to uniquely identify a channel upon creation

Exceptions:
InputError - Occurs when:
    - Channel_id does not refer to a valid channel

AccessError - Occurs when:
    - The channel_id is valid but the authorised user is not a member of the channel

Return Value:
    returns a dictionary containing basic details of a channel with the given channel_id including
    the channel name, if the channel is private or public, the list of owner members and the list of all members
'''
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
def messages_channel_v1(auth_user_id, channel_id, start):
    store = data_store.get()
    
    channel = get_channel(channel_id, store)
    check_authorised_user(auth_user_id, channel_id, store)

    len_message_channel = len(channel['messages'])

    pagination = messages_pagination(len_message_channel, start)
    # #goes through the messages in a 0 - 50, 50 - 100, 100 - 150, in pagination 
    # #manner, always starting from the first index and then continuing on the 
    # #following call
    message_list = []
    for i in range(start, pagination['page_length']):
        message_list.append(channel['messages'][pagination['len_message_channel_dm'] - i]) 
    
    #returning a single dictionary with a key that is a list.
    return {
        'messages': message_list, 
        'start': start,
        'end': pagination['end'],
    }

def messages_dm_v1(auth_user_id, dm_id, start):
    store = data_store.get()

    dm = check_dm_id_exists(dm_id, store)
    check_user_in_dm(auth_user_id, dm)
    
    len_message_dm = len(dm['messages'])

    pagination = messages_pagination(len_message_dm, start)
    # #goes through the messages in a 0 - 50, 50 - 100, 100 - 150, in pagination 
    # #manner, always starting from the first index and then continuing on the 
    # #following call
    message_list = []
    for i in range(start, pagination['page_length']):
        message_list.append(dm['messages'][pagination['len_message_channel_dm'] - i]) 
    
    #returning a single dictionary with a key that is a list. 
    return {
        'messages': message_list, 
        'start': start,
        'end': pagination['end'],
    }
'''
Allows user to join a channel is a member

Arguments:
    auth_user_id (int) - the id of the authorised user that is to join the channel.
    channel_id (int) - the id of the channel that authorised user is to join.

Exceptions:
    InputError - Occurs when any of:
        - channel_id does not refer to a valid channel
        - The authorised user is already a member of the channel
    AccessError - Occurs when:
        - channel_id refers to a channel that is private and the authorised user is not already a channel member and is not a global owner

Return Value = {}
'''
def channel_join_v1(auth_user_id, channel_id):
    store = data_store.get()
    
    # Checks if user exists and if so stores location in list
    user_join = find_user(auth_user_id, store)
    
    # Check if channel_id valid 
    check_channel_id(channel_id, store)

    # Stores location of channel in list
    channel_join = find_channel(channel_id, store)
    
    # If channel is private and user is not global owner
    # prevent user from joining 
    if channel_join['is_public'] == False and user_join['is_streams_owner'] == False:
        raise AccessError
        
    # Check if user is already member of channel
    check_authorised_member(auth_user_id, channel_id, store)    
    
    # Create member dictionary  
    member_dictionary = {
        "u_id": user_join['u_id']
    }
    
    # Append user id to member list
    channel_join['all_members'].append(member_dictionary)
    
    data_store.set(store)
    return {}

'''
Allows user to leave a channel 

Arguments:
    auth_user_id (int) - the id of the authorised user that is to leave the channel.
    channel_id (int) - the id of the channel that authorised user is to leave

Exceptions:
    InputError - Occurs when any of:
        - channel_id does not refer to a valid channel
    AccessError - Occurs when:
        - channel_id is valid and the authorised user is not a member of the channel

Return Value = {}
'''
def channel_leave_v1(auth_user_id, channel_id):
    store = data_store.get()
    

    # Checks if user exists and if so stores location in list
    find_user(auth_user_id, store)
    
    # Check if channel_id valid 
    check_channel_id(channel_id, store)

    # Stores location of channel in list
    channel = find_channel(channel_id, store)
    
    
    for owner in channel['owner_members']:
        if auth_user_id == owner['u_id']:       
            channel['owner_members'].remove(owner)
            
    # Remove the member from the channel 
    for member in channel['all_members']:
        if member['u_id'] == auth_user_id:
            channel['all_members'].remove(member)
            data_store.set(store)
            return {}
    raise AccessError(description = 'Cannot leave channel you have not joined')
    
'''
Make user with user id u_id an owner of the channel

Arguments:
    auth_user_id (int) - the id of the authorised user that is promoting a member
    channel_id (int) - the id of the channel where the promotion is to occur
    u_id (int) - the id of the user to be promoted  


Exceptions:
    InputError - Occurs when any of:
        - channel_id does not refer to a valid channel
        - u_id does not refer to a valid user
        - u_id refers to a user who is not a member of the channel
        - u_id refers to a user who is already an owner of the channel

    AccessError - Occurs when:
        - channel_id is valid and the authorised user does not have owner permissions in the channel

Return Value = {}
'''  

def channel_addowner_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()
    
    # Checks if user exists and if so stores location in list
    user = find_user(auth_user_id, store)
    
    # Check if channel_id valid 
    check_channel_id(channel_id, store)

    # Stores location of channel in list
    channel = find_channel(channel_id, store)

    # Checks if user with u_id is already an owner of the channel
    for owner in channel['owner_members']:
        if u_id == owner['u_id']: 
            raise InputError(description='User with u_id is already an owner of the channel')
   
    if auth_user_id not in channel['owner_members'] and user['is_streams_owner'] == False:
        raise AccessError(description='auth_user is not an owner of the channel or an owner of streams')

    for member in channel['all_members']:
        if member['u_id'] == u_id:
            channel['owner_members'].append({'u_id': u_id})
            data_store.set(store)
            return {}
    raise InputError(description = 'Not a member of the channel cannot be promoted')
   
'''
Remove user with user id u_id as an owner of the channel

Arguments:
    auth_user_id (int) - the id of the authorised user that is promoting a member
    channel_id (int) - the id of the channel where the promotion is to occur
    u_id (int) - the id of the user to be promoted  


Exceptions:
    InputError - Occurs when any of:
        - channel_id does not refer to a valid channel
        - u_id does not refer to a valid user
        - u_id refers to a user who is not an owner of the channel
        - u_id refers to a user who is currently the only owner of the channel

    AccessError - Occurs when:
        - channel_id is valid and the authorised user does not have owner permissions in the channel

Return Value = {}
'''    
def channel_removeowner_v1(auth_user_id, channel_id, u_id):
    store = data_store.get()
    
    # Checks if user exists and if so stores location in list
    user = find_user(auth_user_id, store)
    
    # Check if channel_id valid 
    check_channel_id(channel_id, store)

    # Stores location of channel in list
    channel = find_channel(channel_id, store)

    # user with u_id is not an owner of the channel
    found = False
    for owner in channel['owner_members']:
        if owner['u_id'] == u_id:
            found = True

    if found == False:
        raise InputError(description = 'CUser with u_id is not an owner of the channel')

    found1 = False
    for owner in channel['owner_members']:
        if owner['u_id'] == auth_user_id:
            found1 = True

    if found1 == False and user['is_streams_owner'] == False:
          raise AccessError(description='Bauth_user is not an owner of the channel or an owner of streams')
    #if auth_user_id not in channel['owner_members'] and user['is_streams_owner'] == False:
       # raise AccessError(description='Bauth_user is not an owner of the channel or an owner of streams')

    # user with u_id is the only owner of the channel
    if len(channel['owner_members']) == 1:
        raise InputError(description='AUser with u_id is the only owner of the channel')


    new_owner_list = [owner_dict for owner_dict in channel['owner_members'] if owner_dict.get('u_id') != u_id]
    for channel in store['channels']:
        if channel_id == channel['channel_id']: 
            channel['owner_members'] = new_owner_list

    data_store.set(store)
    return {}
    