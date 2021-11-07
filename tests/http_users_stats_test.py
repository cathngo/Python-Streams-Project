import pytest
import requests
import json
from src import config
import jwt

#check stats are 0 when streams owner first registers
def test_initalise_stats():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #get token from auth reg
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user_token['token']})
    r = resp.json()
    assert r['workspace_stats']['channels_exist'][0]['num_channels_exist'] == 0
    assert r['workspace_stats']['dms_exist'][0]['num_dms_exist'] == 0
    assert r['workspace_stats']['messages_exist'][0]['num_messages_exist'] == 0

def test_correct_utilization_rate():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register three users
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid1email@gmail.com', 'password': '123abc!@#', 'name_first': 'Becky', 'name_last': 'Smile'})
    requests.post(config.url + 'auth/register/v2', json={'email': 'valid2email@gmail.com', 'password': '123abc!@#', 'name_first': 'George', 'name_last': 'Peach'})
    user1_token = user1.json()
    user2_token = user2.json()
    #create a channel
    channel1 = requests.post(config.url + 'channels/create/v2', json={'token': user1_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel1_id = channel1.json() 
    #user 1 join a channel
    requests.post(config.url + 'channel/join/v2', json={'token': user1_token['token'], 'channel_id': channel1_id['channel_id']})
    #user1 and user_2 join dm
    requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user2_token['auth_user_id']],
    })
    #get users stats
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #rate = 2 users joined atleast one channel/dm / 3 users
    assert r['workspace_stats']['utilization_rate'] == float(2/3)

def test_correct_channels_exist():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register one users
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create three channels
    requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Snow', 'is_public': True})
    requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Bean', 'is_public': True})
    #get users stats
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user_token['token']})
    r = resp.json()
    #assert latest record is 3 channels
    assert r['workspace_stats']['channels_exist'][-1]['num_channels_exist'] == 3

def test_correct_dms_exist():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register three users
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid1email@gmail.com', 'password': '123abc!@#', 'name_first': 'Becky', 'name_last': 'Smile'})
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid2email@gmail.com', 'password': '123abc!@#', 'name_first': 'George', 'name_last': 'Peach'})
    user1_token = user1.json()
    user2_token = user2.json()
    user3_token = user3.json()
    #create three dms
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user2_token['auth_user_id']],
    })
    requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user3_token['auth_user_id']],
    })
    requests.post(config.url + 'dm/create/v1', json={
        'token': user2_token['token'],
        'u_ids': [user3_token['auth_user_id']],
    })
    dm_reg = dm.json()

    #remove one dm
    requests.delete(config.url + 'dm/remove/v1', json={
        'token': user1_token['token'],
        'dm_id': dm_reg['dm_id'],
    })
    #get users stats
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #assert latest record is 2 dms
    assert r['workspace_stats']['dms_exist'][-1]['num_dms_exist'] == 2


def test_correct_messages_exist():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #Register threeusers
    user1 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'valid1email@gmail.com', 'password': '123abc!@#', 'name_first': 'Becky', 'name_last': 'Smile'})
    user1_token = user1.json()
    user2_token = user2.json()
    #create a dms
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user1_token['token'],
        'u_ids': [user2_token['auth_user_id']],
    })
    dm_reg = dm.json()
    #send two msgs
    msg1 = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1_token['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    requests.post(config.url + 'message/senddm/v1', json={
        'token': user1_token['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "helloagain",
    })
    msg1_id = msg1.json()
    #remove one message
    requests.delete(config.url + 'message/remove/v1', json={ 
        'token': user1_token['token'],
        'message_id': msg1_id['message_id'], 
    })  
    #get user stats
    resp = requests.get(config.url + 'users/stats/v1', params={'token': user1_token['token']})
    r = resp.json()
    #sent two msgs, removed a msg so total msgs is now 1
    assert r['workspace_stats']['messages_exist'][-1]['num_messages_exist'] == 1
