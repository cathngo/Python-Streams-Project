import requests
import json
from src import config
import jwt


#check 
def test_basic_listall():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'San'})
    user_token = user.json()
    requests.post(config.url + 'channels/create/v2',json={'token': user_token['token'],'name': 'Fox' , 'is_public' : True})

    re = requests.get(config.url + 'channels/listall/v2', params={'token': user_token['token']})
    ch_dict = re.json()
    assert len(ch_dict['channels']) == 1
    
#check when the list is empty 
def test_empty_listall_v2():
    #reset route
    requests.delete(config.url + 'clear/v1')
    
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'San'})
    user_token = user.json()
    re = requests.get(config.url + 'channels/listall/v2', params={'token': user_token['token']})
    ch_dict = re.json()
    
    assert len(ch_dict['channels']) == 0
    
def test_multiple_channels_and_usersall_v2():
    #reset route
    requests.delete(config.url + 'clear/v1')
    
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'San'})
    user_token = user.json()
    user_2 = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail2@gmail.com', 'password': '123abc!@#2', 'name_first': 'Masoko', 'name_last': 'West'})
    user_token2 = user_2.json()
    
    requests.post(config.url + 'channels/create/v2',json={'token': user_token['token'],'name': 'Fox' , 'is_public' : True})
    requests.post(config.url + 'channels/create/v2',json={'token': user_token['token'],'name': 'Fox2' , 'is_public' : False})
    requests.post(config.url + 'channels/create/v2',json={'token': user_token2['token'],'name': 'Fox3' , 'is_public' : True})
    requests.post(config.url + 'channels/create/v2',json={'token': user_token2['token'],'name': 'Fox4' , 'is_public' : False})
    
    re = requests.get(config.url + 'channels/listall/v2', params={'token': user_token['token']})
    ch_dict = re.json()
    
    assert len(ch_dict['channels']) == 4
    
def test_invalid_token_listall():
#reset route
    requests.delete(config.url + 'clear/v1')
    
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Kanye', 'name_last': 'San'})
    user_token = user.json()
    invalid_u_id = user_token['auth_user_id'] + 1
    invalid_token = jwt.encode({'u_id': invalid_u_id, 'session_id': 0}, config.SECRET, algorithm='HS256')
    
    requests.post(config.url + 'channels/create/v2',json={'token': user_token['token'],'name': 'Fox' , 'is_public' : True})
    
    re = requests.get(config.url + 'channels/listall/v2', params={'token': invalid_token})
    
    assert re.status_code == 403
