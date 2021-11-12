import time
import pytest
import requests
import json
from src import config
from datetime import datetime
from tests.pytest_fixtures import (
    clear, reg_user1, reg_user2, reg_channel_user1, send_channel_message_user1, 
    send_dm_message_user1, reg_dm_user1, reg_dm_2users, 
    user1_react_to_their_message_in_channel, user1_react_to_their_message_in_dm,
    user2_react_to_user1_message_in_dm, user2_react_to_user1_message_in_channel,
    send_channel_message_with_two_users_user1, send_dm_message_user1_in_dm_with_two_users, 
    user2_channel_join
)
from src.error import InputError, AccessError

def test_route_works_message_send_later():
    requests.delete(config.url + 'clear/v1')

    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()

    user2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail12@gmail.com', 
        'password': '122abc!@#', 
        'name_first': 'Tomas', 
        'name_last': 'Lam'
    })
    user_token2 = user2.json()    

    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': user_token['token'], 
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id = channel.json()

    requests.post(config.url + 'channel/invite/v2',json={
        'token': user_token['token'],
        'channel_id': channel_id['channel_id'], 
        'u_id': user_token2['auth_user_id']
    })
    
    resp = requests.post(config.url + 'message/sendlater/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'message': "@" + "tomaslam",
        'time_sent': int(datetime.now().timestamp()) + 1,
        'is_pinned': False,
        'reacts':[
                {
                    'react_id': 1,
                    'u_ids': [], 
                    'is_this_user_reacted': False
                }
            ]
    })

    time.sleep(1) 

    r1 = requests.get(config.url + 'channel/messages/v2', params={
        'token': user_token['token'], 
        'channel_id': channel_id['channel_id'],
        'start': 0,
    })
    payload = r1.json()

    r4 = requests.get(config.url + '/notifications/get/v1', params={
        'token': user_token2['token']
    })
    payload4 = r4.json()
    assert len(payload4['notifications']) == 2
    assert len(payload['messages']) == 1

    assert resp.status_code == 200

def test_dm_create_works():
    
    #Check if dm/create/v1 returns expected output
    
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Kanye',
        'name_last': 'East',
    })
    r9 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user3@email.com',
        'password': 'user3password',
        'name_first': 'Kanyeet',
        'name_last': 'Left',
    })    
    payload1 = r1.json()
    payload2 = r2.json()
    payload9 = r9.json()

    r3 = requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [payload2['auth_user_id'], payload9['auth_user_id']],
    })

    r4 = requests.get(config.url + '/notifications/get/v1', params={
        'token': payload2['token']
    })
    payload4 = r4.json()
    
    r5 = requests.get(config.url + '/notifications/get/v1', params={
        'token': payload9['token']
    })    
    payload5 = r5.json()
    
    assert r3.status_code == 200
    assert r4.status_code == 200
    assert len(payload4['notifications']) == 1
    assert len(payload5['notifications']) == 1


def test_invite_private_channel_v2():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail12@gmail.com', 'password': '122abc!@#2', 'name_first': 'Tomas', 'name_last': 'Lam'})
    user_token2 = user2.json()
  
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': False})
    channel_id = channel.json()
    requests.post(config.url + 'channel/invite/v2',json={'token': user_token['token'],'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})

    resp = requests.get(config.url + 'channel/details/v2', params={'token': user_token['token'], 'channel_id': channel_id['channel_id']})
    #get the response in json
    res = resp.json()

    r4 = requests.get(config.url + '/notifications/get/v1', params={
        'token': user_token2['token']
    })
    payload4 = r4.json()
    assert len(res['all_members']) == 2
    assert len(payload4['notifications']) == 1


def test_user2_react_to_user1_message_in_channel_is_true(
    clear, reg_user2, reg_user1, reg_channel_user1, user2_react_to_user1_message_in_channel
    ):
    channel_id = reg_channel_user1
    user1 = reg_user1

    message_page = requests.get(config.url + 'channel/messages/v2', params={
        'token': user1['token'], 
        'channel_id': channel_id,
        'start': 0,
    })
    message_list = message_page.json()

    r4 = requests.get(config.url + '/notifications/get/v1', params={
        'token': user1['token']
    })
    payload4 = r4.json()
    assert len(payload4['notifications']) == 1
        
    assert message_list['messages'][0]['reacts'][0]['is_this_user_reacted'] == True

