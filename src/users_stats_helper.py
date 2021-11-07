from datetime import datetime
from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle

def create_workspace_stats(u_id, store):
    time_created = int(datetime.now().timestamp())

    store['workspace_stats'] = {
        'channels_exist': [{'num_channels_exist': 0, 'time_stamp': time_created}],
        'dms_exist': [{'num_dms_exist': 0, 'time_stamp': time_created}],
        'messages_exist': [{'num_messages_exist': 0, 'time_stamp': time_created}],
        'utilization_rate': 0, 
    }

def update_channels_exist(store, increment):
    time_created = int(datetime.now().timestamp())
    #get latest count
    recent = store['workspace_stats']['channels_exist'][-1]
    new_count = recent['num_channels_exist'] + increment
    store['workspace_stats']['channels_exist'].append({'num_channels_exist': new_count, 'time_stamp': time_created})

def update_dms_exist(store, increment):
    time_created = int(datetime.now().timestamp())
    #get latest count
    recent = store['workspace_stats']['dms_exist'][-1]
    new_count = recent['num_dms_exist'] + increment
    store['workspace_stats']['dms_exist'].append({'num_dms_exist': new_count, 'time_stamp': time_created})

def update_messages_exist(store, increment):
    time_created = int(datetime.now().timestamp())
    #get latest count
    recent = store['workspace_stats']['messages_exist'][-1]
    new_count = recent['num_messages_exist'] + increment
    store['workspace_stats']['messages_exist'].append({'num_messages_exist': new_count, 'time_stamp': time_created})

def get_workspace_stats(store):
    store = open_pickle()
    num_channel_dm = 0
    for user in store['all_user_stats']:
        if user['user_stats']['channels_joined'][-1]['num_channels_joined'] > 0 or user['user_stats']['dms_joined'][-1]['num_dms_joined'] > 0:
            num_channel_dm += 1
    
    num_users =  0
    for user in store['users']:
        num_users += 1
    
    utilization = num_channel_dm/num_users

    store['workspace_stats']['utilization_rate'] = float(utilization)
    return store['workspace_stats']