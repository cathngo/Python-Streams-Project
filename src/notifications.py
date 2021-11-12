from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
from src.channel_details_helper import get_user_details
from src.channel_messages_helper import get_channel, check_message_is_right_character_length
from src.dm_helper import check_dm_id_exists, check_user_in_dm
from src.channels_invite_helper import check_u_id_exists

def identify_tag(auth_user_id, channel_id, dm_id, message, message_id):
    store = open_pickle()
    name = ''
    for user in store['users']:
        handle = "@" + user['handle_str']
        users_handle = get_user_details(auth_user_id, store)['handle_str']
        if handle in message: 
            if channel_id != -1 and dm_id == -1:
                name = get_channel(channel_id, store)["name"]
            elif channel_id == -1 and dm_id != -1:
                name = check_dm_id_exists(dm_id, store)["name"]
        
            notif = f"{users_handle} tagged you in {name}: {message[0:20]}"
 
            user["notifications"].append(
                {
                "channel_id": channel_id,
                "dm_id": dm_id,
                "notification_message": notif
                }
            )
 
    data_store.set(store)
    save_pickle()

def identify_react_notification(auth_user_id, u_id, channel_id, dm_id, message_id):

    store = open_pickle()
    name = ''
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            users_handle = get_user_details(auth_user_id, store)['handle_str']
            if channel_id != -1 and dm_id == -1:
                name = get_channel(channel_id, store)["name"]
            elif channel_id == -1 and dm_id != -1:
                name = check_dm_id_exists(dm_id, store)["name"]
            

            notif = f"{users_handle} reacted to your message in {name}"

    for user1 in store['users']:
        if user1['u_id'] == u_id:
            user1["notifications"].append(
                {
                "channel_id": channel_id,
                "dm_id": dm_id,
                "notification_message": notif
                }
            )
 
    data_store.set(store)
    save_pickle()

def identify_add(auth_user_id, u_id, channel_id, dm_id):
    
    store = open_pickle()
    name = ''
    for user in store['users']:
        if user['u_id'] == auth_user_id:
            users_handle = get_user_details(auth_user_id, store)['handle_str']
            if channel_id != -1 and dm_id == -1:
                name = get_channel(channel_id, store)["name"]
            elif channel_id == -1 and dm_id != -1:
                name = check_dm_id_exists(dm_id, store)["name"]
            
            notif = f"{users_handle} added you to {name}"

    for user1 in store['users']:
        if user1['u_id'] == u_id:
            user1["notifications"].append(
                {
                "channel_id": channel_id,
                "dm_id": dm_id,
                "notification_message": notif
                }
            )
            data_store.set(store)
            save_pickle() 

    data_store.set(store)
    save_pickle()    


def notifications_get_v1(auth_user_id):
    store = open_pickle()
    check_u_id_exists(auth_user_id, store)
    user_notifs = get_user_details(auth_user_id, store)['notifications']
    if len(user_notifs) >= 20:
        return {'notifications': user_notifs[0:20]}
    else:
        return {'notifications': user_notifs} 
   