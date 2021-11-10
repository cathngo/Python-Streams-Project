from datetime import datetime
from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle

def create_workspace_stats(store):
    '''
Intialises workspace stats to 0 when the streams owner registers

Arguments:
    store (dictionary) - the database which stores the workspace stats

Return Value: 
    Returns void 
'''
    time_created = int(datetime.now().timestamp())

    store['workspace_stats'] = {
        'channels_exist': [{'num_channels_exist': 0, 'time_stamp': time_created}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': time_created}],
        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': time_created}],
        'utilization_rate': 0, 
    }

def update_channels_exist(store, increment):
    '''
Adds a new timestamp to channels_exist for workspace stats

Arguments:
    store (dictionary) - the database which stores the workspace stats
    increment (int) - the amount of channels created 

Return Value: 
    Returns void 
'''
    time_created = int(datetime.now().timestamp())
    #get latest count
    recent = store['workspace_stats']['channels_exist'][-1]
    new_count = recent['num_channels_exist'] + increment
    store['workspace_stats']['channels_exist'].append({'num_channels_exist': new_count, 'time_stamp': time_created})

def update_dms_exist(store, increment):
    '''
Adds a new timestamp to dms_exist for the workspace stats

Arguments:
    store (dictionary) - the database which stores the workspace stats
    increment (int) - the amount of dms created/removed (negative if a dm has been removed)

Return Value: 
    Returns void 
'''
    time_created = int(datetime.now().timestamp())
    #get latest count
    recent = store['workspace_stats']['dms_exist'][-1]
    new_count = recent['num_dms_exist'] + increment
    store['workspace_stats']['dms_exist'].append({'num_dms_exist': new_count, 'time_stamp': time_created})

def update_messages_exist(store, increment):
    '''
Adds a new timestamp to messages_exist for the workspace stats

Arguments:
    store (dictionary) - the database which stores the workspace stats
    increment (int) - the amount of messages created/removed (negative if a message has been removed)

Return Value: 
    Returns void 
'''
    time_created = int(datetime.now().timestamp())
    #get latest count
    recent = store['workspace_stats']['messages_exist'][-1]
    new_count = recent['num_messages_exist'] + increment
    store['workspace_stats']['messages_exist'].append({'num_messages_exist': new_count, 'time_stamp': time_created})

def update_messages_exist_sent_later(time_created, store, increment):
    '''
Adds a new timestamp to messages_exist for the workspace stats

Arguments:
    time_created (integer unix timestamp) - the time the message was sent
    store (dictionary) - the database which stores the workspace stats
    increment (int) - the amount of messages created/removed (negative if a message has been removed)

Return Value: 
    Returns void 
'''
    time_created = int(datetime.now().timestamp())
    #get latest count
    recent = store['workspace_stats']['messages_exist'][-1]
    new_count = recent['num_messages_exist'] + increment
    store['workspace_stats']['messages_exist'].append({'num_messages_exist': new_count, 'time_stamp': time_created})


def get_workspace_stats(store):
    '''
Returns the workspace stats

Arguments:
    store (dictionary) - the database which stores the workspace stats

Return Value: 
    Returns a dictionary containing the current workspace stats
'''
    store = open_pickle()
    num_channel_dm = 0
    for user in store['all_user_stats']:
        if user['user_stats']['channels_joined'][-1]['num_channels_joined'] > 0 or user['user_stats']['dms_joined'][-1]['num_dms_joined'] > 0:
            num_channel_dm += 1
    
    num_users =  0
    for user in store['users']:
        if user['name_first'] != 'Removed':
            num_users += 1
    
    utilization = num_channel_dm/num_users

    store['workspace_stats']['utilization_rate'] = float(utilization)
    #store['workspace_stats']['utilization_rate'] = num_channel_dm
    return store['workspace_stats']