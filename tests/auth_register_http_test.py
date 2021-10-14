import requests
import jwt

BASE_URL = 'http://127.0.0.1:1024'

def test_correct_id():
    '''
    Checks if registered users are assigned unqiue ids
    '''
    r1 = requests.post(f'{BASE_URL}/auth_register', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(f'{BASE_URL}/auth_register', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Lavar',
        'name_last': 'Ball',
    })
    payload1 = r1.json()
    payload2 = r2.json()

    assert payload1['auth_user_id'] != payload2['auth_user_id']


def test_correct_token():
    '''
    Checks if registered user is assigned correct token
    '''
    r = requests.post(f'{BASE_URL}/auth_register', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload = r.json()
    user_info = jwt.decode(payload['token'], 'Kanye', algorithms=['HS256'])
    assert user_info['auth_user_id'] == payload['auth_user_id']