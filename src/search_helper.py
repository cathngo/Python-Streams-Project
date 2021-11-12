from src.error import InputError

def messages_in_channel(u_id: int, query: str, channels: list):
    if len(query) > 1000 or len(query) < 1:
        raise InputError(description="Length of the is less than 1 or over 1000 characters")
    return_list = []
    #check all channels
    for channel in channels:
        #if u_id is part of the channel
        if u_id in [d['u_id'] for d in channel['all_members']]:
            for current_message in channel['messages']:
                #check if the given query is a substring of the current message
                if current_message['message'].find(query) != -1:
                    return_list.append(current_message.copy())

    return return_list

def messages_in_dms(u_id, query, dms):
    return_list = []
    #check all dms
    for dm in dms:
        #u_id not member of the dm
        if u_id not in dm['members']: continue

        for current_message in dm['messages']:
            #check if the given query is a substring of the current message
            if current_message['message'].find(query) != -1:
                return_list.append(current_message.copy())

    return return_list