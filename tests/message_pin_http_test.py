import pytest
import requests
import json
from src import config
import jwt
from src.error import InputError, AccessError
from tests.pytest_fixtures import (
    clear, reg_user1, reg_user2, reg_channel_user1, send_channel_message_user1, 
    send_channel_message_user2, send_dm_message_user1, reg_dm_user1, reg_dm_2users, 
    send_dm_message_user1_in_dm_with_two_users, user2_channel_join,send_dm_message_user2_in_dm_with_two_users, 
    reg_channel_user2, send_dm_message_user2, reg_dm_user2, send_channel_message_with_two_users_user1,
    owner_pins_their_message_in_dm, owner_pins_their_message_in_channel, owner_pins_user2_message_in_dm, 
    owner_pins_user1_message_in_channel, streams_owner_pins_owner_message_in_channel, user1_channel_join,
    send_channel_message_user1_in_user2_channel, send_channel_message_user2_in_user2_channel, 
)

def test_invalid_token_message_pin(clear, reg_user1, send_channel_message_user1):
    user1 = reg_user1
    message_id = send_channel_message_user1
    #create invalid token
    invalid_token = jwt.encode({'u_id': user1['auth_user_id'], 'session_id': 0}, 'Invalid', algorithm='HS256')
    #pin message with the invalid token
    pin = requests.post(config.url + 'message/pin/v1', json={ 
        'token': invalid_token,
        'message_id': message_id
    })
    assert pin.status_code == AccessError.code

#message_id is not a valid message within a DM that the authorised user has joined
def test_message_id_not_in_dm_message_pin(clear, reg_user1, reg_dm_user1):
    user1 = reg_user1
    invalid_message_id = 1000
    #pin to message with the invalid message_id
    pin = requests.post(config.url + 'message/pin/v1', json={ 
        'token': user1['token'],
        'message_id': invalid_message_id,
    })  
    assert pin.status_code == InputError.code 

#message_id is not a valid message within a channel that the authorised user has joined
def test_message_id_not_in_channel_message_pin(clear, reg_user1, reg_channel_user1):
    user1 = reg_user1
    invalid_message_id = 1000
    #pin to message with the invalid message_id
    pin = requests.post(config.url + 'message/pin/v1', json={ 
        'token': user1['token'],
        'message_id': invalid_message_id,
    })  
    assert pin.status_code == InputError.code

def test_streams_owner_tries_to_pin_to_a_message_in_a_channel_they_are_not_a_member_of(
    clear, reg_user1, send_channel_message_user2
    ): 
    user1 = reg_user1
    message_id = send_channel_message_user2

    pin = requests.post(config.url + 'message/pin/v1', json={ 
        'token': user1['token'],
        'message_id': message_id, 
    })
    assert pin.status_code == InputError.code

def test_streams_owner_tries_to_pin_to_a_message_in_a_dm_they_are_not_a_member_of(
    clear, reg_user1, send_dm_message_user2
    ): 
    user1 = reg_user1
    message_id = send_dm_message_user2

    pin = requests.post(config.url + 'message/pin/v1', json={ 
        'token': user1['token'],
        'message_id': message_id, 
    })
    assert pin.status_code == InputError.code

#the message is already pinned in dm
def test_message_already_pinned_by_user_in_dm(
    clear, reg_user1, send_dm_message_user1, owner_pins_their_message_in_dm
    ):
    user1 = reg_user1
    message_id = send_dm_message_user1
    pinned = requests.post(config.url + 'message/pin/v1', json={ 
        'token': user1['token'],
        'message_id': message_id, 
    })
    assert pinned.status_code == InputError.code 

#the message is already pinned in channel
def test_message_already_pinned_by_user_in_channel(
    clear, reg_user1, send_channel_message_user1, owner_pins_their_message_in_channel
    ):
    user1 = reg_user1
    message_id = send_channel_message_user1
    pinned = requests.post(config.url + 'message/pin/v1', json={ 
        'token': user1['token'],
        'message_id': message_id, 
    })
    assert pinned.status_code == InputError.code 
    
#message_id refers to a valid message in a joined DM and the authorised user does not have owner permissions in the DM
def test_user_does_not_have_owner_permissions_to_pin_message_in_dm(
    clear, reg_user2, send_dm_message_user1_in_dm_with_two_users
    ):
    user2 = reg_user2
    message_id = send_dm_message_user1_in_dm_with_two_users
    pin = requests.post(config.url + 'message/pin/v1', json={ 
        'token': user2['token'],
        'message_id': message_id, 
    })
    assert pin.status_code == AccessError.code 

#message_id refers to a valid message in a joined channel and the authorised user does not have owner permissions in the channel
def test_user_does_not_have_owner_permissions_to_pin_message_in_channel(
    clear, send_channel_message_with_two_users_user1, reg_user2
    ):
    message_id = send_channel_message_with_two_users_user1
    user2 = reg_user2
    pin = requests.post(config.url + 'message/pin/v1', json={ 
        'token': user2['token'],
        'message_id': message_id, 
    })
    assert pin.status_code == AccessError.code 

def test_streams_owner_can_pin_message_in_channel(
    clear, reg_user1, reg_channel_user2, streams_owner_pins_owner_message_in_channel
    ):
    user1 = reg_user1
    channel_id = reg_channel_user2
    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user1['token'], 
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = message_page.json()
    assert message_list['messages'][0]['is_pinned'] == True

def test_owner_can_pin_message_in_channel(
    clear, reg_user2, reg_channel_user2, owner_pins_user1_message_in_channel
    ):
    user2 = reg_user2
    channel_id = reg_channel_user2
    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user2['token'], 
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = message_page.json()
    assert message_list['messages'][0]['is_pinned'] == True

def test_owner_can_pin_message_in_dm(
    clear, reg_user1, reg_dm_2users, owner_pins_user2_message_in_dm
    ):
    user1 = reg_user1
    dm_id = reg_dm_2users
    message_page = requests.get(config.url + 'dm/messages/v1', params={
        'token': user1['token'], 
        'dm_id': dm_id['dm_id'],
        'start': 0,
    })
    message_list = message_page.json()
    assert message_list['messages'][0]['is_pinned'] == True