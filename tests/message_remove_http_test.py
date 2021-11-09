import pytest
import requests
import json
from src import config
import jwt
from tests.pytest_fixtures import (
    clear, reg_user1, reg_user2, reg_channel_user1, send_channel_message_user1, 
    send_dm_message_user1, reg_dm_user1, reg_dm_2users, send_dm_message_user1_in_dm_with_two_users,
    user2_channel_join, send_channel_message_with_two_users_user2, 
    send_dm_message_user2_in_dm_with_two_users
)
from src.error import InputError, AccessError

def test_valid_token_message_remove(clear, reg_user1, send_channel_message_user1):
    #register user 
    user_token = reg_user1
    message_id = send_channel_message_user1
    #create invalid token
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    #remove message with the invalid token
    removed = requests.delete(config.url + 'message/remove/v1', json={ 
        'token': invalid_token,
        'message_id': message_id,
    })
    #get the response from the server for the message
    assert removed.status_code == AccessError.code 

def test_message_id_not_in_dm_message_remove(clear, reg_user1, reg_dm_user1):
    #register user 
    user_token = reg_user1
    #register the user into a dm
    invalid_message_id = 1000
    #remove message with the invalid message_id
    removed = requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token['token'],
        'message_id': invalid_message_id,
    })  
    assert removed.status_code == InputError.code


def test_message_id_not_in_channel_message_remove(clear, reg_user1, reg_channel_user1):
    user_token = reg_user1
    invalid_message_id = 1000
    #remove message with the invalid message_id
    removed = requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token['token'],
        'message_id': invalid_message_id,
    })  
    assert removed.status_code == InputError.code


def test_member_did_not_send_the_dm_message_remove(
    clear, reg_user2, send_dm_message_user1_in_dm_with_two_users
    ):
    user2_token = reg_user2
    message_id = send_dm_message_user1_in_dm_with_two_users
    #user2 attempts to remove message sent by user 1
    removed = requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user2_token['token'],
        'message_id': message_id,
    })  
    #get the response from the server for the message
    assert removed.status_code == AccessError.code 

def tests_member_message_was_removed_message_member_removed_channel(
    clear, reg_user1, reg_channel_user1, reg_user2, user2_channel_join
):
    user_token = reg_user1
    #create a channel with that user
    channel_id = reg_channel_user1
    #create a user
    user_token2 = reg_user2
    
    requests.post(config.url + 'message/send/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id,
        'message': "hello",
    })
    message_send2 = requests.post(config.url + 'message/send/v1', json={
        'token': user_token2['token'], 
        'channel_id': channel_id,
        'message': "hello",
    })
    message_id1 = message_send2.json()
    
    #the channel owner removes the message   
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token2['token'],
        'message_id': message_id1['message_id'], 
    })  

    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token2['token'], 
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = message_page.json()

    assert len(message_list['messages']) == 1
    
def tests_member_message_was_removed_message_member_removed_dm(
    clear, reg_user2, reg_user1, reg_dm_2users,
):
    #create a user
    user_token = reg_user1
    #create a user
    user_token2 = reg_user2
    #create a dm with those users
    dm_id = reg_dm_2users
    #the member user sends a message to channel
    message_send1 = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_token['token'], 
        'dm_id': dm_id['dm_id'],
        'message': "hello",
    })
    message_send2 = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_token2['token'], 
        'dm_id': dm_id['dm_id'],
        'message': "hello",
    })
    message_id1 = message_send1.json()
    message_id2 = message_send2.json()
    #the channel owner removes the message   
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token2['token'],
        'message_id': message_id2['message_id'], 
    })
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id1['message_id'], 
    })

    message_page = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_token2['token'], 
        'dm_id': dm_id['dm_id'],
        'start': 0,
    })
    message_list = message_page.json()

    assert len(message_list['messages']) == 0

def test_owner_can_remove_message_from_member_channel_message_remove(
    clear, reg_user1, reg_user2, reg_channel_user1, send_channel_message_with_two_users_user2
):  
    user_token = reg_user1
    user_token2 = reg_user2
    channel_id = reg_channel_user1
    message_id = send_channel_message_with_two_users_user2

    #the channel owner removes the message   
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id, 
    })  

    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token2['token'], 
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = message_page.json()

    assert len(message_list['messages']) == 0

def test_member_message_was_removed_by_owner_removed_dm(
    clear, reg_user1, reg_user2, reg_dm_2users, send_dm_message_user2_in_dm_with_two_users
):
    user_token = reg_user1
    user_token2 = reg_user2
    dm_id = reg_dm_2users
    message_id = send_dm_message_user2_in_dm_with_two_users
    
    #the channel owner removes the message   
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id, 
    })  

    message_page = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_token2['token'], 
        'dm_id': dm_id['dm_id'],
        'start': 0,
    })
    message_list = message_page.json()

    assert len(message_list['messages']) == 0