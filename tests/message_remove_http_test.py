import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt
from src.data_store import data_store

def test_valid_token_message_remove():
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
    #remove message with the invalid token
    removed = requests.delete(config.url + 'message/remove/v1', json={ 
        'token': invalid_token,
        'message_id': message_id,
    })
    #get the response from the server for the message
    assert removed.status_code == 403 

def test_message_id_not_in_dm_message_remove():

    requests.delete(config.url + 'clear/v1')
    #register user 
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    invalid_message_id = 1000
    #remove message with the invalid message_id
    removed = requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token['token'],
        'message_id': invalid_message_id,
    })  
    assert removed.status_code == 400 

def test_member_did_not_send_the_dm_message_remove():

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
    #user2 attempts to remove message sent by user 1
    removed = requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user2_token['token'],
        'message_id': message_id,
    })  
    #get the response from the server for the message
    assert removed.status_code == 403 

def test_member_did_not_send_the_channel_message_remove():
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
    #register channel with user
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()
    
    requests.post(config.url + 'channels/join/v2', json={
        'token': user_token['token'], 
        'channel_id': channel_id
    })
    
    #send_message with the user
    message_send = requests.post(config.url + 'message/send/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    
    #user2 attempts to remove message sent by user 1
    removed = requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user2_token['token'],
        'message_id': message_id,
    })  

    assert removed.status_code == 403

def tests_route_works_dm_message_remove():
    requests.delete(config.url + 'clear/v1')
 
    #register user 
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #register dm 
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_token['token'], 
        'u_ids': [],
    })
    dm_id = dm.json()
    #send_message
    message_send = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_token['token'], 
        'dm_id': dm_id['dm_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    #remove message
    removed = requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id,
    })  
    #get the response from the server for the message
    assert removed.status_code == 200

def tests_route_works_channel_message_remove():
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
    
    #send_message
    message_send = requests.post(config.url + 'message/send/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    
    #remove message
    removed = requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id,
    })  
    #get the response from the server for the message remove
    assert removed.status_code == 200

def tests_message_was_removed_message_removed_dm():
    requests.delete(config.url + 'clear/v1')
 
    #register user 
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    #register dm 
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user_token['token'], 
        'u_ids': [],
    })
    dm_id = dm.json()
    #send_message
    message_send = requests.post(config.url + 'message/senddm/v1', json={
        'token': user_token['token'], 
        'dm_id': dm_id['dm_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    #remove message
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id,
    })  
    #check that the list is 0, meaning that the message was removed

    assert len(message_id) == 0

def tests_message_was_removed_message_removed_channel():
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
    
    #send_message
    message_send = requests.post(config.url + 'message/send/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    
    #remove message
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id,
    })  
    #check that the list is 0, meaning that the message was removed
    assert len(message_id) == 0

def test_owner_can_remove_message_from_member_dm_message_remove():
    requests.delete(config.url + 'clear/v1')
    #register owner 
    owner = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    owner_token = owner.json()
    #register member
    member = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail2@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam2', 
        'name_last': 'Smith'
    })
    member_token = member.json()
    
    #register dm with the member being invited to it 
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': owner_token['token'], 
        'u_ids': [member_token['auth_user_id']],
    })
    dm_reg = dm.json()

    #the second user sends a message to dm
    message_send = requests.post(config.url + 'message/senddm/v1', json={
        'token': member_token['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    message_id = message_send.json()
    #the dm owner removes the message 
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': owner_token['token'],
        'message_id': message_id,
    })  
    #check that the list is 0, meaning that the message was removed
    assert len(message_id) == 0

def test_owner_can_remove_message_from_member_channel_message_remove():  
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
    
    #the channel owner removes the message   
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user_token['token'],
        'message_id': message_id['message_id'], 
    })  

    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token2['token'], 
        'channel_id': channel_id['channel_id'],
        'start': 0,
    })
    message_list = message_page.json()

    assert len(message_list['messages']) == 0