import pytest
import requests
import json
from src import config
import jwt
from src.error import InputError, AccessError
from tests.pytest_fixtures import (
    clear, reg_user1, reg_user2, reg_channel_user1, send_channel_message_user1, 
    send_dm_message_user1, reg_dm_user1, reg_dm_2users, 
    user1_react_to_their_message_in_channel, user1_react_to_their_message_in_dm,
    user2_react_to_user1_message_in_dm, user2_react_to_user1_message_in_channel,
    send_channel_message_with_two_users_user1, send_dm_message_user1_in_dm_with_two_users, 
    user2_channel_join
)

def test_invalid_token_message_react(clear, reg_user1, send_channel_message_user1):
    user1 = reg_user1
    message_id = send_channel_message_user1
    #create invalid token
    invalid_token = jwt.encode({'u_id': user1['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    #react to message with the invalid token
    react = requests.post(config.url + 'message/react/v1', json={ 
        'token': invalid_token,
        'message_id': message_id,
        'react_id': 1   
    })
    assert react.status_code == AccessError.code 

#test message_id is not a valid message within a DM that the authorised user has joined
def test_message_id_not_in_dm_message_react(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    invalid_message_id = 1000
    #react to message with the invalid message_id
    react = requests.post(config.url + 'message/react/v1', json={ 
        'token': user1['token'],
        'message_id': invalid_message_id,
        'react_id':0
    })  
    assert react.status_code == InputError.code 

#test message_id is not a valid message within a channel that the authorised user has joined
def test_message_id_not_in_channel_message_react(clear, reg_user1, reg_channel_user1):
    user1 = reg_user1
    invalid_message_id = 1000
    #react to message with the invalid message_id
    react = requests.post(config.url + 'message/react/v1', json={ 
        'token': user1['token'],
        'message_id': invalid_message_id,
        'react_id': 1
    })  
    assert react.status_code == InputError.code

#react_id is not a valid react ID in channel
def test_react_id_not_in_channel_message_react(clear, reg_user1, send_channel_message_user1):
    user1 = reg_user1
    message_id = send_channel_message_user1
    react = requests.post(config.url + 'message/react/v1', json={ 
        'token': user1['token'],
        'message_id': message_id,
        'react_id': 2       
    })
    assert react.status_code == InputError.code 

#react_id is not a valid react ID in dm
def test_react_id_not_in_dm_message_react(clear, reg_user1, send_dm_message_user1):
    user1 = reg_user1
    message_id = send_dm_message_user1
    react = requests.post(config.url + 'message/react/v1', json={ 
        'token': user1['token'],
        'message_id': message_id,
        'react_id': 2       
    })
    assert react.status_code == InputError.code 

# the message already contains a react with ID react_id from the authorised user in dm
def test_react_message_alreaded_react_to_in_by_user_in_dm(
    clear, reg_user1, send_dm_message_user1, user1_react_to_their_message_in_dm
    ):
    user1 = reg_user1
    message_id = send_dm_message_user1
    reacted = requests.post(config.url + 'message/react/v1', json={ 
        'token': user1['token'],
        'message_id': message_id,
        'react_id': 1      
    })
    assert reacted.status_code == InputError.code 
    
# the message already contains a react with ID react_id from the authorised user in channel
def test_react_message_alreaded_react_to_in_by_user_in_channel(
    clear, reg_user1, send_channel_message_user1, user1_react_to_their_message_in_channel
    ):
    user1 = reg_user1
    message_id = send_channel_message_user1
    reacted = requests.post(config.url + 'message/react/v1', json={ 
        'token': user1['token'],
        'message_id': message_id,
        'react_id': 1     
    })
    assert reacted.status_code == InputError.code 
    
def test_user1_reacted_to_their_message_in_channel_is_true(
    clear, reg_user1, reg_channel_user1, user1_react_to_their_message_in_channel
    ):
    user1 = reg_user1
    channel_id = reg_channel_user1

    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user1['token'], 
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = message_page.json()
    
    assert message_list['messages'][0]['reacts'][0]['is_this_user_reacted'] == True

def test_user1_reacted_to_their_message_in_dm_is_true(
    clear, reg_user1, reg_dm_user1, user1_react_to_their_message_in_dm
    ):
    user1 = reg_user1
    dm_id = reg_dm_user1

    message_page = requests.get(config.url + 'dm/messages/v1', params={
        'token': user1['token'], 
        'dm_id': dm_id['dm_id'],
        'start': 0,
    })
    message_list = message_page.json()
    
    assert message_list['messages'][0]['reacts'][0]['is_this_user_reacted'] == True

def test_user2_react_to_user1_message_in_dm_is_true(
    clear, reg_user2, reg_dm_2users, user2_react_to_user1_message_in_dm
    ):
    user2 = reg_user2
    dm_id = reg_dm_2users

    message_page = requests.get(config.url + 'dm/messages/v1', params={
        'token': user2['token'], 
        'dm_id': dm_id['dm_id'],
        'start': 0,
    })
    message_list = message_page.json()
    
    assert message_list['messages'][0]['reacts'][0]['is_this_user_reacted'] == True

def test_user2_react_to_user1_message_in_channel_is_true(
    clear, reg_user2, reg_user1, reg_channel_user1, user2_react_to_user1_message_in_channel
    ):
    channel_id = reg_channel_user1
    user1 =  reg_user1

    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user1['token'], 
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = message_page.json()
    
    print(message_list)
    
    assert message_list['messages'][0]['reacts'][0]['is_this_user_reacted'] == True