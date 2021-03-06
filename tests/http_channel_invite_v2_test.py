import pytest
import requests
import json
from src import config
from src.other import clear_v1
import jwt
from src.error import AccessError, InputError


#check valid token 
def test_given_token():
    requests.delete(config.url + 'clear/v1')
    #create user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    #create invalid token
    invalid_token = jwt.encode({'u_id': user_token['auth_user_id'], 'session_id': 0}, 'invalid', algorithm='HS256')
    re = requests.post(config.url + 'channel/invite/v2', json={'token': invalid_token, 'channel_id': channel_id['channel_id']})
    assert re.status_code == AccessError.code


#check
def test_invalid_channel_id():
    requests.delete(config.url + 'clear/v1')
    #create user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Rambo', 'name_last': 'Smith'})
    user_token = user.json()
    invalid_channel_id = 9999
    #create a user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail1@gmail.com', 'password': '122abc!@#', 'name_first': 'Tam', 'name_last': 'Lam'})
    user_token2 = user2.json()
    
    re = requests.post(config.url + 'channel/invite/v2', json={'token': user_token['token'],'channel_id': invalid_channel_id , 'u_id': user_token2['auth_user_id']})
    assert re.status_code == InputError.code

#check inviting to private channel
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

    assert len(res['all_members']) == 2
    
#check invalid u_id
def test_invite_invalid_u_id_v2():
    requests.delete(config.url + 'clear/v1')
    invalid_u_id = 9999
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': False})
    channel_id = channel.json()
    
    re = requests.post(config.url + 'channel/invite/v2',json={'token': user_token['token'],'channel_id': channel_id['channel_id'], 'u_id': invalid_u_id})

    assert re.status_code == InputError.code

#check invalid u_id
def test_invite_another_member_v2():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create another use
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail12@gmail.com', 'password': '122abc!@#2', 'name_first': 'Tomas', 'name_last': 'Lam'})
    user_token2 = user2.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': False})
    channel_id = channel.json()
    #invite the same suer twice
    requests.post(config.url + 'channel/invite/v2',json={'token': user_token['token'],'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})
    re = requests.post(config.url + 'channel/invite/v2',json={'token': user_token['token'],'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})

    assert re.status_code == InputError.code

#check error when valid channel but inviter is not member
def test_invitation_not_authorised():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create another use
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail12@gmail.com', 'password': '122abc!@#2', 'name_first': 'Tomas', 'name_last': 'Lam'})
    user_token2 = user2.json()
    #create another use
    user3 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail3@gmail.com', 'password': '122abc!@#2', 'name_first': 'Samor', 'name_last': 'Narco'})
    user_token3 = user3.json()
    #create a channel with that user
    channel = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    channel_id = channel.json()
    #invite the same suer twice
    re = requests.post(config.url + 'channel/invite/v2',json={'token': user_token3['token'],'channel_id': channel_id['channel_id'], 'u_id': user_token2['auth_user_id']})

    assert re.status_code == AccessError.code

# Check if invite works when there are multiple channels
def test_multiple_channel_invite_once_works():
    requests.delete(config.url + 'clear/v1')
    #create a user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #create another user
    user2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail12@gmail.com', 'password': '122abc!@#2', 'name_first': 'Tomas', 'name_last': 'Lam'})
    user_token2 = user2.json()
    #create multiple channels with user1
    requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca', 'is_public': True})
    requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Alpaca1', 'is_public': True})
    r = requests.post(config.url + 'channels/create/v2', json={'token': user_token['token'], 'name': 'Hello', 'is_public': True})
    payload = r.json()
    #invite user2 to channel 2
    re = requests.post(config.url + 'channel/invite/v2',json={'token': user_token['token'],'channel_id': payload['channel_id'], 'u_id': user_token2['auth_user_id']})

    assert re.status_code == 200
