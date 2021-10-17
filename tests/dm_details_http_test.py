import requests
from src import config

def test_dm_details_works():
    '''
    Check if dm/details/v1 returns expected output
    '''
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
    payload1 = r1.json()
    payload2 = r2.json()

    r3 = requests.post(config.url + 'dm/create/v1', json={
        'token': payload1['token'],
        'u_ids': [payload2['auth_user_id']],
    })
    payload3 = r3.json()
    
    r4 = requests.get(config.url + 'dm/details/v1', params={
        'token': payload1['token'],
        'dm_id': payload3['dm_id'],
    })
    payload4 = r4.json()
    assert len(payload4['members']) == 2

# def test_invalid_token():
#     '''
#     Check if invalid token is passed as input
#     '''
#     requests.delete(config.url + 'clear/v1')
#     r1 = requests.post(config.url + 'auth/register/v2', json={
#         'email': 'user1@email.com',
#         'password': 'user1password',
#         'name_first': 'Kanye',
#         'name_last': 'Yeezus',
#     })
#     payload1 = r1.json()

#     r2 = requests.post(config.url + 'dm/create/v1', json={
#         'token': payload1['token'],
#         'u_ids': [],
#     })
#     payload2 = r2.json()

#     r3 = requests.get(config.url + 'dm/details/v1', params={
#         'token': 'invalidtoken',
#         'dm_id': payload2['dm_id'],
#     })
#     assert r3.status_code == 403


# def test_invalid_dm_id():
#     '''
#     Check if invalid dm_id is passed as input
#     '''
#     requests.delete(config.url + 'clear/v1')
#     r1 = requests.post(config.url + 'auth/register/v2', json={
#         'email': 'user1@email.com',
#         'password': 'user1password',
#         'name_first': 'Kanye',
#         'name_last': 'Yeezus',
#     })
#     payload1 = r1.json()

#     r2 = requests.post(config.url + 'dm/create/v1', json={
#         'token': payload1['token'],
#         'u_ids': [],
#     })
#     payload2 = r2.json()

#     r3 = requests.get(config.url + 'dm/details/v1', params={
#         'token': payload1['token'],
#         'dm_id': payload2['dm_id'] + 1,
#     })
#     assert r3.status_code == 400

# def test_not_dm_member():
#     '''
#     Check when dm_id is valid and the authorised user is not a member of the DM
#     '''
#     requests.delete(config.url + 'clear/v1')
#     r1 = requests.post(config.url + 'auth/register/v2', json={
#         'email': 'user1@email.com',
#         'password': 'user1password',
#         'name_first': 'Kanye',
#         'name_last': 'Yeezus',
#     })
#     r2 = requests.post(config.url + 'auth/register/v2', json={
#         'email': 'user2@email.com',
#         'password': 'user2password',
#         'name_first': 'Kanye',
#         'name_last': 'East',
#     })
#     payload1 = r1.json()
#     payload2 = r2.json()

#     r3 = requests.post(config.url + 'dm/create/v1', json={
#         'token': payload1['token'],
#         'u_ids': [],
#     })
#     payload3 = r3.json()
    
#     r4 = requests.get(config.url + 'dm/details/v1', params={
#         'token': payload2['token'],
#         'dm_id': payload3['dm_id'],
#     })
#     assert r4.status_code == 403