from datetime import datetime
from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle

def get_user_stats(u_id):
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
    
    involvement = numerator/denominator

    if denominator == 0:
        involvement = 0
    
    if involvement > 1:
        involvement = 1

    #update involvment
    store['all_user_stats']

    #now return stats
    for user in store['all_user_stats']:
        if user['u_id'] == u_id:
            user['user_stats']['involvement_rate'] = float(involvement)
            return user['user_stats']

#initalize stats - initalise stats to 0 when user is first registered into database
def create_user_stats(u_id, store):
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
    time_created = int(datetime.now().timestamp())
    for user in store['all_user_stats']:
        if user['u_id'] == u_id:
            #get the last dictionary value in the list
            recent = user['user_stats']['dms_joined'][-1]
            #increment the count if it increases dm joined (dmcreate) or decrement it (dm/leave or dm/remove) 
            new_count = recent['num_dms_joined'] + increment
            user['user_stats']['dms_joined'].append({'num_dms_joined': new_count, 'time_stamp': time_created})
