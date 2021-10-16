import requests
import jwt
from src import config

def test_unique_id():
    '''
    Checks if registered users are assigned unqiue ids
    '''
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Lavar',
        'name_last': 'Ball',
    })
    payload1 = r1.json()
    payload2 = r2.json()

    user1_info = jwt.decode(payload1['token'], 'Kanye', algorithms=['HS256'])
    user2_info = jwt.decode(payload2['token'], 'Kanye', algorithms=['HS256'])
    assert user1_info['auth_user_id'] != user2_info['auth_user_id']


def test_correct_token():
    '''
    Checks if registered users are assigned a unique token
    '''
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Lavar',
        'name_last': 'Ball',
    })
    payload1 = r1.json()
    payload2 = r2.json()

    assert payload1['token'] != payload2['token']

def test_unique_session_id():
    '''
    Checks if registered users are assigned unique session id's
    '''
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Lavar',
        'name_last': 'Ball',
    })
    payload1 = r1.json()
    payload2 = r2.json()

    user1_info = jwt.decode(payload1['token'], 'Kanye', algorithms=['HS256'])
    user2_info = jwt.decode(payload2['token'], 'Kanye', algorithms=['HS256'])
    assert user1_info['session_id'] != user2_info['session_id']

def test_unique_invalid_email():
    '''
    Check if email entered is invalid
    '''
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'bademailcom',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    assert r1.status_code == 400

def test_register_duplicate_email():
    '''
    Check if email address is already being used by another user
    '''
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user2password',
        'name_first': 'Lavar',
        'name_last': 'Ball',
    })
    assert r2.status_code == 400

def test_register_password_length():
    '''
    Check if length of password is less than 6 characaters
    '''
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'pw',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    assert r1.status_code == 400

def test_register_fname_length():
    '''
    Check if length of name_first is not between 1 and 50 characters inclusive
    '''
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': '',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user2password',
        'name_first': 'ffffff' * 10,
        'name_last': 'Ball',
    })
    assert r1.status_code == 400
    assert r2.status_code == 400

def test_register_lname_length():
    '''
    Check if length of name_last is not between 1 and 50 characters inclusive
    '''
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': '',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user2password',
        'name_first': 'Lavar',
        'name_last': 'ffffff' * 10,
    })
    assert r1.status_code == 400
    assert r2.status_code == 400