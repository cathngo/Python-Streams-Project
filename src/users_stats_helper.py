from datetime import datetime
from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle

def create_workspace_stats(u_id, store):
    time_created = int(datetime.now().timestamp())

    store['workspace_stats'] = {
        'channels_exist': [{'num_channels_exist': 1, 'time_stamp': time_created}],
        'dms_exist': [{'num_dms_exist': 1, 'time_stamp': time_created}],
        'messages_exist': [{'num_messages_exist': 1, 'time_stamp': time_created}],
        'utilization_rate': 0, 
    }