from datetime import datetime
from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle

def get_user_stats(u_id):
    '''
Returns the user's stats for the given user

Arguments:
    u_id (int) - the id of the user whose stats are being retrieved

Return Value: 
    Returns a dictionary containing the user's stats
'''
    store = open_pickle()
    
    #first get numerator 
    num_channels_joined = 0
    num_dms_joined = 0
    num_msgs_sent = 0
    for user in store['all_user_stats']:
        if user['u_id'] == u_id:
            #get num channels
            num_channels_joined = user['user_stats']['channels_joined'][-1]['num_channels_joined']
            #get num dms
            num_dms_joined = user['user_stats']['dms_joined'][-1]['num_dms_joined']
            #get num msgs
            num_msgs_sent = user['user_stats']['messages_sent'][-1]['num_messages_sent']
    list_num = [num_channels_joined, num_dms_joined, num_msgs_sent]
    numerator = sum(list_num)

    #then get denominator
    num_channels = store['workspace_stats']['channels_exist'][-1]['num_channels_exist']
    num_dms = store['workspace_stats']['dms_exist'][-1]['num_dms_exist']
    num_msgs = store['workspace_stats']['messages_exist'][-1]['num_messages_exist']
    list_denom = [num_channels, num_dms, num_msgs]
    denominator = sum(list_denom)

    if denominator == 0:
        involvement = 0
    elif numerator/denominator > 1:
        involvement = 1
    else:
        involvement = numerator/denominator

    #update involvment
    store['all_user_stats']

    #now return stats
    for user in store['all_user_stats']:
        if user['u_id'] == u_id:
            user['user_stats']['involvement_rate'] = float(involvement)
            return user['user_stats']


def create_user_stats(u_id, store):
    '''
Intialises a user's stats to 0 when they are first registered

Arguments:
    u_id (int) - the id of the user whose stats are being created
    store (dictionary) - the database which stores the user's stats

Return Value: 
    Returns void 
'''
    time_created = int(datetime.now().timestamp())
    store['all_user_stats'].append({
        'u_id': u_id,
        'user_stats': {
            'channels_joined': [{'num_channels_joined': 0, 'time_stamp': time_created}],
            'dms_joined': [{'num_dms_joined': 0, 'time_stamp': time_created}],
            'messages_sent': [{'num_messages_sent': 0, 'time_stamp': time_created}],
            'involvement_rate': 0, 
        },
    })


def update_channels_joined(u_id, store, increment):
    '''
Adds a new timestamp to channels_joined for the user's stats

Arguments:
    u_id (int) - the id of the user whose stats are being updated
    store (dictionary) - the database which stores the user's stats
    increment (int) - the amount of channels the user has joined (negative if they have left a channel)

Return Value: 
    Returns void 
'''
    #for channel join
    time_created = int(datetime.now().timestamp())
    for user in store['all_user_stats']:
        if user['u_id'] == u_id:
            #get the last dictionary value in the list
            recent = user['user_stats']['channels_joined'][-1]
            #increment the count if it increases channels joined (channeljoin /channelcreate function)or decrement it (channelleave) 
            new_count = recent['num_channels_joined'] + increment
            user['user_stats']['channels_joined'].append({'num_channels_joined': new_count, 'time_stamp': time_created})

def update_dms_joined(u_id, store, increment):
    '''
Adds a new timestamp to dms_joined for the user's stats

Arguments:
    u_id (int) - the id of the user whose stats are being updated
    store (dictionary) - the database which stores the user's stats
    increment (int) - the amount of dms the user has joined (negative if they have left a dm or the dm has been removed)

Return Value: 
    Returns void 
'''
    time_created = int(datetime.now().timestamp())
    for user in store['all_user_stats']:
        if user['u_id'] == u_id:
            #get the last dictionary value in the list
            recent = user['user_stats']['dms_joined'][-1]
            #increment the count if it increases dm joined (dmcreate) or decrement it (dm/leave or dm/remove <- need to double check for dmremove)
            new_count = recent['num_dms_joined'] + increment
            user['user_stats']['dms_joined'].append({'num_dms_joined': new_count, 'time_stamp': time_created})

#this will only ever increase message count for user stats
def update_messages_sent(u_id, store, increment):
    '''
Adds a new timestamp to messages_sent for the user's stats 

Arguments:
    u_id (int) - the id of the user whose stats are being updated
    store (dictionary) - the database which stores the user's stats
    increment (int) - the amount of messages the user has sent

Return Value: 
    Returns void 
'''
    time_created = int(datetime.now().timestamp())
    for user in store['all_user_stats']:
        if user['u_id'] == u_id:
            #get the last dictionary value in the list
            recent = user['user_stats']['messages_sent'][-1]
            #increment the count if it increases msgs sent (message/senddm, message/send)
            new_count = recent['num_messages_sent']  + increment
            user['user_stats']['messages_sent'].append({'num_messages_sent': new_count, 'time_stamp': time_created})


def remove_user_stats(u_id, store):
    '''
Remove the user's stats if they have been removed from Streams

Arguments:
    u_id (int) - the id of the user whose stats are being updated
    store (dictionary) - the database which stores the user's stats

Return Value: 
    Returns void 
'''
    for user in store['all_user_stats']:
        if user['u_id'] == u_id:
            #remove the user
            store['all_user_stats'].remove(user)

#this will only ever increase message count for user stats
def update_messages_sent_later(time_created, u_id, store, increment):
    '''
Adds a new timestamp to messages_sent for the user's stats 

Arguments:
    time_created (integer unix timestamp) - the time the message was sent
    u_id (int) - the id of the user whose stats are being updated
    store (dictionary) - the database which stores the user's stats
    increment (int) - the amount of messages the user has sent

Return Value: 
    Returns void 
'''
    for user in store['all_user_stats']:
        if user['u_id'] == u_id:
            #get the last dictionary value in the list
            recent = user['user_stats']['messages_sent'][-1]
            #increment the count if it increases msgs sent (message/senddm, message/send)
            new_count = recent['num_messages_sent']  + increment
            user['user_stats']['messages_sent'].append({'num_messages_sent': new_count, 'time_stamp': time_created})
