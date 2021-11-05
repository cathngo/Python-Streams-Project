import pytest
import requests
import json
from src import config
import jwt
from src.error import InputError, AccessError
from tests.pytest_fixtures import (
    clear, reg_user1, reg_user2, reg_channel_user1, send_channel_message_user1, 
    send_channel_message_user2, send_dm_message_user1, reg_dm_user1, reg_dm_2users, 
    send_dm_message_user1_in_dm_with_two_users, user2_channel_join, send_channel_message_with_two_users_user2, 
    send_dm_message_user2_in_dm_with_two_users
)

def test_valid_token_message_edit(clear, reg_user1, send_channel_message_user1):
    user1 = reg_user1
    #register channel 
    message_id = send_channel_message_user1
    #create invalid token
    invalid_token = jwt.encode({'u_id': user1['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    #edit message with the invalid token
    editd = requests.put(config.url + 'message/edit/v1', json={ 
        'token': invalid_token,
        'message_id': message_id,
        'message': "goodbye"       
    })
    #get the response from the server for the message
    assert editd.status_code == AccessError.code 

def test_message_id_not_in_dm_message_edit(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    invalid_message_id = 1000
    #edit message with the invalid message_id
    editd = requests.put(config.url + 'message/edit/v1', json={ 
        'token': user1['token'],
        'message_id': invalid_message_id,
        'message':"goodbye"
    })  
    assert editd.status_code == InputError.code 

def test_message_id_not_in_channel_message_edit(clear, reg_user1, reg_channel_user1):
    user1 = reg_user1
    invalid_message_id = 1000
    #edit message with the invalid message_id
    editd = requests.put(config.url + 'message/edit/v1', json={ 
        'token': user1['token'],
        'message_id': invalid_message_id,
        'message':"goodbye"
    })  
    assert editd.status_code == InputError.code

def test_member_did_not_send_the_dm_message_edit(clear, reg_user2, 
send_dm_message_user1_in_dm_with_two_users
):
    user2 = reg_user2
    message_id = send_dm_message_user1_in_dm_with_two_users
    #user2 attempts to edit message sent by user 1
    editd = requests.put(config.url + 'message/edit/v1', json={ 
        'token': user2['token'],
        'message_id': message_id,
        'message':"goodbye"
    })  
    #get the response from the server for the message
    assert editd.status_code == AccessError.code 

def tests_member_message_was_editd_message_member_editd_channel(
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
        'message': "hi",
    })
    requests.post(config.url + 'message/send/v1', json={
        'token': user_token2['token'], 
        'channel_id': channel_id,
        'message': "hi",
    })
    requests.post(config.url + 'message/send/v1', json={
        'token': user_token2['token'], 
        'channel_id': channel_id,
        'message': "hi",
    })
    message_send = requests.post(config.url + 'message/send/v1', json={
        'token': user_token2['token'], 
        'channel_id': channel_id,
        'message': "hello",
    })
    message_id = message_send.json()
    
    #the channel owner edits the message   
    requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token2['token'],
        'message_id': message_id['message_id'],
        'message': "goodbye" 
    })  

    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token2['token'], 
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = message_page.json()

    assert message_list['messages'][0]['message'] == "goodbye"
    
def tests_member_message_was_editd_message_member_editd_dm(
    clear, reg_user2, reg_dm_2users, send_dm_message_user1_in_dm_with_two_users
):
    #create a user
    user_token2 = reg_user2
    #create a dm with those users
    dm_id = reg_dm_2users
    #the member user sends a message to channel
    send_dm_message_user1_in_dm_with_two_users
    
    message_send = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_token2['token'], 
        'dm_id': dm_id['dm_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    #the channel owner edits the message   
    requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token2['token'],
        'message_id': message_id['message_id'], 
        'message': "goodbye"
    })  
    message_page = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_token2['token'], 
        'dm_id': dm_id['dm_id'],
        'start': 0,
    })
    message_list = message_page.json()

    assert message_list['messages'][0]['message'] == "goodbye"

def test_owner_can_edit_message_from_member_channel_message_edit(
    clear, reg_user1, reg_channel_user1, reg_user2, send_channel_message_with_two_users_user2
    ):  
    user_token = reg_user1
    #create a channel with that user
    channel_id = reg_channel_user1
    #create a user
    user_token2 = reg_user2
    message_id = send_channel_message_with_two_users_user2

    #the channel owner edits the message   
    requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id,
        'message': "goodbye" 
    })  

    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token2['token'], 
        'channel_id': channel_id,
        'start': 0
    })
    message_list = message_page.json()

    assert message_list['messages'][0]['message'] == "goodbye"

def test_member_message_was_editd_by_owner_editd_dm(
    clear, reg_user2, reg_user1, reg_dm_2users, send_dm_message_user2_in_dm_with_two_users
):  
    user_token = reg_user1
    #create a user
    user_token2 = reg_user2
    #create a dm with those users
    dm_id = reg_dm_2users
    #the member user sends a message to channel
    message_id = send_dm_message_user2_in_dm_with_two_users
    #the channel owner edits the message   
    requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id,
        'message': "goodbye"
    })  

    message_page = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_token2['token'], 
        'dm_id': dm_id['dm_id'],
        'start': 0,
    })
    message_list = message_page.json()

    assert message_list['messages'][0]['message'] == "goodbye"

def tests_member_message_was_deleted_by_empty_string_message_member_edit_dm(
    clear, reg_user2, reg_user1, reg_dm_2users, send_dm_message_user2_in_dm_with_two_users
):
    user_token = reg_user1
    #create a user
    user_token2 = reg_user2
    #create a dm with those users
    dm_id = reg_dm_2users
    #the member user sends a message to channel
    message_id = send_dm_message_user2_in_dm_with_two_users

    #the channel owner edits the message   
    requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id, 
        'message': ""
    })  

    message_page = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_token2['token'], 
        'dm_id': dm_id['dm_id'],
        'start': 0,
    })
    message_list = message_page.json()
    assert (message_list['messages']) == []

def tests_member_message_was_deleted_by_empty_string_message_member_edit_channel(
    clear, reg_user1, reg_channel_user1, reg_user2, send_channel_message_with_two_users_user2
):
    user_token = reg_user1
    #create a channel with that user
    channel_id = reg_channel_user1
    #create a user
    user_token2 = reg_user2
    
    message_id = send_channel_message_with_two_users_user2
    #the channel owner edits the message   
    requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id,
        'message':"" 
    })  

    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token2['token'], 
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = message_page.json()

    assert (message_list['messages']) == []

def tests_member_message_is_greater_than_one_thousand_characters_member_editd_dm(
    clear, reg_user2, reg_dm_2users
    ):
    #create a user
    user_token2 = reg_user2
    #create a dm with those users
    dm_id = reg_dm_2users
    #the member user sends a message to channel
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user_token2['token'], 
        'dm_id': dm_id['dm_id'],
        'message': "hi",
    })
    message_send = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_token2['token'], 
        'dm_id': dm_id['dm_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    
    #the channel owner edits the message   
    resp = requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token2['token'],
        'message_id': message_id['message_id'], 
        'message': "f" * 1001
    })  
    assert resp.status_code == InputError.code