import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt

def test_valid_token_message_edit():
    requests.delete(config.url + 'clear/v1')
    #register user 
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #register channel 
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    #send message in channle
    message_send = requests.post(config.url + 'message/send/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    #create invalid token
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    #edit message with the invalid token
    editd = requests.put(config.url + 'message/edit/v1', json={ 
        'token': invalid_token,
        'message_id': message_id,
        'message':"goodbye"       
    })
    #get the response from the server for the message
    assert editd.status_code == 403 

def test_message_id_not_in_dm_message_edit():
    requests.delete(config.url + 'clear/v1')
    #register user 
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    
    #register the user into a dm
    requests.post(config.url + 'dm/create/v1', json={
        'token': user_token['token'], 
        'u_ids': [],
    })
    
    invalid_message_id = 1000
    #edit message with the invalid message_id
    editd = requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token['token'],
        'message_id': invalid_message_id,
        'message':"goodbye"
    })  
    assert editd.status_code == 400 

def test_message_id_not_in_channel_message_edit():
    requests.delete(config.url + 'clear/v1')
    #register user 
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    
    requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    
    invalid_message_id = 1000
    #edit message with the invalid message_id
    editd = requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token['token'],
        'message_id': invalid_message_id,
        'message':"goodbye"
    })  
    assert editd.status_code == 400

def test_member_did_not_send_the_dm_message_edit():

    requests.delete(config.url + 'clear/v1')
    #register user 
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #register user2
    user2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail2@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam2', 
        'name_last': 'Smith'
    })
    user2_token = user2.json()
    #register users to the dm
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_token['token'], 
        'u_ids': [user2_token['auth_user_id']],
    })
    dm_reg = dm.json()
    #send_message with the user
    message_send = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_token['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    #user2 attempts to edit message sent by user 1
    editd = requests.put(config.url + 'message/edit/v1', json={ 
        'token': user2_token['token'],
        'message_id': message_id,
        'message':"goodbye"
    })  
    #get the response from the server for the message
    assert editd.status_code == 403 

def tests_member_message_was_editd_message_member_editd_channel():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 
        'password': '122abc!@#', 
        'name_first': 'Tam', 
        'name_last': 'Lam'
    })
    user_token2 = user2.json()
    
    requests.post(config.url + 'channel/join/v2', json={
        'token': user_token2['token'], 
        'channel_id': channel_id['channel_id']
    })
    
    #the member user sends a message to channel
    message_send = requests.post(config.url + 'message/send/v1', json={
        'token': user_token2['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    
    #the channel owner edits the message   
    requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token2['token'],
        'message_id': message_id['message_id'],
        'message':"goodbye" 
    })  

    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token2['token'], 
        'channel_id': channel_id['channel_id'],
        'start': 0,
    })
    message_list = message_page.json()

    assert message_list['messages'][0]['message'] == "goodbye"
    
def tests_member_message_was_editd_message_member_editd_dm():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()

    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail1@gmail.com', 
        'password': '122abc!@#', 
        'name_first': 'Tam', 
        'name_last': 'Lam'
    })
    user_token2 = user2.json()

    #create a dm with those users
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_token['token'], 
        'u_ids': [user_token2['auth_user_id']],
    })
    dm_id = dm.json()
    #the member user sends a message to channel
    
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

def test_owner_can_edit_message_from_member_channel_message_edit():  
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 
        'password': '122abc!@#', 
        'name_first': 'Tam', 
        'name_last': 'Lam'
    })
    user_token2 = user2.json()
    
    requests.post(config.url + 'channel/join/v2', json={
        'token': user_token2['token'], 
        'channel_id': channel_id['channel_id']
    })
    
    #the member user sends a message to channel
    message_send = requests.post(config.url + 'message/send/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    
    #the channel owner edits the message   
    requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id['message_id'],
        'message': "goodbye" 
    })  

    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token2['token'], 
        'channel_id': channel_id['channel_id'],
        'start': 0
    })
    message_list = message_page.json()

    assert message_list['messages'][0]['message'] == "goodbye"

def test_member_message_was_editd_by_owner_editd_dm():  
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()

    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail1@gmail.com', 
        'password': '122abc!@#', 
        'name_first': 'Tam', 
        'name_last': 'Lam'
    })
    user_token2 = user2.json()

    #create a dm with those users
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_token['token'], 
        'u_ids': [user_token2['auth_user_id']],
    })
    dm_id = dm.json()
    #the member user sends a message to channel
    
    message_send = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_token2['token'], 
        'dm_id': dm_id['dm_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    
    #the channel owner edits the message   
    requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token['token'],
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

def tests_member_message_was_deleted_by_empty_string_message_member_edit_dm():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()

    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail1@gmail.com', 
        'password': '122abc!@#', 
        'name_first': 'Tam', 
        'name_last': 'Lam'
    })
    user_token2 = user2.json()

    #create a dm with those users
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_token['token'], 
        'u_ids': [user_token2['auth_user_id']],
    })
    dm_id = dm.json()
    #the member user sends a message to channel
    
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
        'message': ""
    })  

    message_page = requests.get(config.url + 'dm/messages/v1', params={
        'token': user_token2['token'], 
        'dm_id': dm_id['dm_id'],
        'start': 0,
    })
    message_list = message_page.json()
    assert (message_list['messages']) == []

def tests_member_message_was_deleted_by_empty_string_message_member_edit_channel():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 
        'password': '122abc!@#', 
        'name_first': 'Tam', 
        'name_last': 'Lam'
    })
    user_token2 = user2.json()
    
    requests.post(config.url + 'channel/join/v2', json={
        'token': user_token2['token'], 
        'channel_id': channel_id['channel_id']
    })
    
    #the member user sends a message to channel
    message_send = requests.post(config.url + 'message/send/v1', json={
        'token': user_token2['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    
    #the channel owner edits the message   
    requests.put(config.url + 'message/edit/v1', json={ 
        'token': user_token2['token'],
        'message_id': message_id['message_id'],
        'message':"" 
    })  

    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token2['token'], 
        'channel_id': channel_id['channel_id'],
        'start': 0,
    })
    message_list = message_page.json()

    assert (message_list['messages']) == []