import pytest
import requests
from src import config

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')

########################################################################
###                     FIXTURES TO REGISTER USER                     
########################################################################

@pytest.fixture
def reg_user1(): 
    user = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token = user.json()
    return user_token

@pytest.fixture
def reg_user2(): 
    user2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'validemail2@gmail.com', 
        'password': '123abc!@#', 
        'name_first': 'Sam', 
        'name_last': 'Smith'
    })
    user_token2 = user2.json()
    return user_token2

########################################################################
###                     FIXTURES TO REGISTER CHANNEL                         
########################################################################

@pytest.fixture
def reg_channel_user1(reg_user1):
    token1 = reg_user1   
    channel = requests.post(config.url + 'channels/create/v2', json={
        'token': token1['token'],
        'name': 'Alpaca', 
        'is_public': True
    })
    channel_id_dic = channel.json()
    channel_id = channel_id_dic['channel_id']
    return channel_id

@pytest.fixture
def reg_channel_user2(reg_user2):
    token2 = reg_user2  
    channel2 = requests.post(config.url + 'channels/create/v2', json={
        'token': token2['token'],
        'name': 'Alpaca', 
        'is_public': True
    })
    channel2_id_dic = channel2.json()
    channel_id2 = channel2_id_dic['channel_id']
    return channel_id2

########################################################################
###                     FIXTURES TO JOIN CHANNEL                         
########################################################################

@pytest.fixture
def user2_channel_join(reg_user2, reg_channel_user1):
    user2 = reg_user2
    channel_id = reg_channel_user1

    requests.post(config.url + 'channel/join/v2', json={
        'token': user2['token'], 
        'channel_id': channel_id
    })
    return 
########################################################################
###                     FIXTURES TO REGISTER DM                         
########################################################################
@pytest.fixture
def reg_dm_user1(reg_user1):
    user1 = reg_user1
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [],
    })
    dm_reg = dm.json()
    return dm_reg

@pytest.fixture
def reg_dm_2users(reg_user1, reg_user2):
    user1 = reg_user1
    user2 = reg_user2
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user1['token'],
        'u_ids': [user2['auth_user_id']],
    })
    dm_reg2_users = dm.json()
    return dm_reg2_users

@pytest.fixture
def reg_dm_user2(reg_user2):
    user2 = reg_user2
    dm = requests.post(config.url + 'dm/create/v1', json={
        'token': user2['token'],
        'u_ids': [],
    })
    dm_reg_user2 = dm.json()
    return dm_reg_user2

########################################################################
###                FIXTURES TO SEND MESSAGE IN DM                         
########################################################################

@pytest.fixture
def send_dm_message_user1(reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    message_id_dic = resp.json()
    message_id = message_id_dic['message_id']
    return message_id

@pytest.fixture
def send_dm_message_user2(reg_user2, reg_dm_user2):
    user2 = reg_user2
    dm_reg2 = reg_dm_user2

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user2['token'], 
        'dm_id': dm_reg2['dm_id'],
        'message': "hello",
    })
    message_id2_dic = resp.json()
    message_id2 = message_id2_dic['message_id']
    return message_id2

@pytest.fixture
def send_2nd_dm_message_user1(reg_user1, reg_dm_user1):
    user1 = reg_user1
    dm_reg = reg_dm_user1

    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    message_id2_dic = resp.json()
    message_id2 = message_id2_dic['message_id']
    return message_id2

@pytest.fixture
def send_dm_message_user1_in_dm_with_two_users(reg_user1, reg_dm_2users):
    user1 = reg_user1
    dm_reg = reg_dm_2users
    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user1['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    message_id_dic = resp.json()
    message_id = message_id_dic['message_id']
    return message_id

@pytest.fixture
def send_dm_message_user2_in_dm_with_two_users(reg_user2, reg_dm_2users):
    user2 = reg_user2
    dm_reg = reg_dm_2users
    resp = requests.post(config.url + 'message/senddm/v1', json={
        'token': user2['token'], 
        'dm_id': dm_reg['dm_id'],
        'message': "hello",
    })
    message_id2_dic = resp.json()
    message_id2 = message_id2_dic['message_id']
    return message_id2

########################################################################
###                FIXTURES TO SEND MESSAGE IN CHANNEL                   
########################################################################

@pytest.fixture
def send_channel_message_user1(reg_user1, reg_channel_user1):
    user1 = reg_user1
    channel_id = reg_channel_user1

    resp = requests.post(config.url + 'message/send/v1', json={
        'token': user1['token'], 
        'channel_id': channel_id,
        'message': "hello",
    })
    message_id_dic = resp.json()
    message_id = message_id_dic['message_id']
    return message_id

@pytest.fixture
def send_2nd_channel_message_user1(reg_user1, reg_channel_user1):
    user1 = reg_user1
    channel_id = reg_channel_user1

    resp = requests.post(config.url + 'message/send/v1', json={
        'token': user1['token'], 
        'channel_id': channel_id,
        'message': "hello",
    })
    message_id2_dic = resp.json()
    message_id2 = message_id2_dic['message_id']
    return message_id2

@pytest.fixture
def send_channel_message_user2(reg_user2, reg_channel_user2):
    user2 = reg_user2
    channel_id2 = reg_channel_user2

    resp = requests.post(config.url + 'message/send/v1', json={
        'token': user2['token'], 
        'channel_id': channel_id2,
        'message': "hello",
    })
    message_id2_dic = resp.json()
    message_id2 = message_id2_dic['message_id']
    return message_id2

@pytest.fixture
def send_channel_message_with_two_users_user2(
    reg_channel_user1, reg_user2, user2_channel_join
):
    channel_id = reg_channel_user1
    user_token2 = reg_user2
    user2_channel_join
    message_send = requests.post(config.url + 'message/send/v1', json={
        'token': user_token2['token'], 
        'channel_id': channel_id,
        'message': "hello",
    })
    message_id_resp = message_send.json()
    message_id = message_id_resp['message_id']
    return message_id
    
@pytest.fixture
def send_channel_message_with_two_users_user1(
    reg_user1, reg_channel_user1, user2_channel_join
):
    user_token = reg_user1
    channel_id = reg_channel_user1
    user2_channel_join
    message_send = requests.post(config.url + 'message/send/v1', json={
        'token': user_token['token'], 
        'channel_id': channel_id,
        'message': "hello",
    })
    message_id_resp = message_send.json()
    message_id = message_id_resp['message_id']

    return message_id

########################################################################
###                FIXTURES TO MESSAGE REACT IN CHANNEL                   
########################################################################
@pytest.fixture
def user1_react_to_their_message_in_channel(reg_user1, send_channel_message_user1):
    user1 = reg_user1
    message_id = send_channel_message_user1
    requests.post(config.url + 'message/react/v1', json={ 
        'token': user1['token'],
        'message_id': message_id,
        'react_id': 1    
    })
    return

@pytest.fixture
def user2_react_to_user1_message_in_channel(reg_user2, send_channel_message_with_two_users_user1):
    user2 = reg_user2
    message_id = send_channel_message_with_two_users_user1
    requests.post(config.url + 'message/react/v1', json={ 
        'token': user2['token'],
        'message_id': message_id,
        'react_id': 1      
    })
    return
########################################################################
###                FIXTURES TO MESSAGE REACT IN DM                   
########################################################################
@pytest.fixture
def user1_react_to_their_message_in_dm(reg_user1, send_dm_message_user1):
    user1 = reg_user1
    message_id = send_dm_message_user1
    requests.post(config.url + 'message/react/v1', json={ 
        'token': user1['token'],
        'message_id': message_id,
        'react_id': 1      
    })
    return

@pytest.fixture
def user2_react_to_user1_message_in_dm(reg_user2, send_dm_message_user1_in_dm_with_two_users):
    user2 = reg_user2
    message_id = send_dm_message_user1_in_dm_with_two_users
    requests.post(config.url + 'message/react/v1', json={ 
        'token': user2['token'],
        'message_id': message_id,
        'react_id': 1      
    })
    return


