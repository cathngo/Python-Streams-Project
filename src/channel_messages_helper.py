from src.error import InputError, AccessError

def get_channel(channel_id, store):
    for channel in store['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    raise InputError(description="Channel was not found")

def messages_pagination(len_message_channel_dm, start):
    #checks that the number of messages has not been over counted or
    #if start is greater than the number of messages in the page
    if start < 0 or start > len_message_channel_dm:
        raise InputError
 
    #checks that the last page is not reached otherwise it continues 
    #that there will be another page to come by not making end = -1.      
    if len_message_channel_dm - start < 50:
        page_length = len_message_channel_dm
        end = -1
    else:
        page_length = 50 + start
        end = page_length
    
    len_message_channel_dm = len_message_channel_dm - 1
   
    #goes through the messages in a 0 - 50, 50 - 100, 100 - 150, in pagination 
    #manner, always starting from the first index and then continuing on the 
    #following call

    return {
        'end': end, 
        'len_message_channel_dm': len_message_channel_dm, 
        'page_length': page_length,
    }

def check_message_is_right_character_length(message_length): 
    if message_length < 1:
        raise InputError(description="Message is less than one character")
    elif message_length > 1000:
        raise InputError(description="Message is over 1000 character") 
    return



