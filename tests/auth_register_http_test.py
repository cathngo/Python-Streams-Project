import requests
import jwt
from src import config
from src.config import SECRET

def test_http_auth_register_works():
    '''
    Checks if auth/register/v2 works
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': '@#!$%^&',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()
    user1_info = jwt.decode(payload1['token'], SECRET, algorithms=['HS256'])
    assert len(user1_info) == 2

def test_http_unique_id():
    '''
    Checks if registered users are assigned unqiue ids
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
        'name_first': 'Lavar',
        'name_last': 'Ball',
    })
    payload1 = r1.json()
    payload2 = r2.json()

    user1_info = jwt.decode(payload1['token'], SECRET, algorithms=['HS256'])
    user2_info = jwt.decode(payload2['token'], SECRET, algorithms=['HS256'])
    assert user1_info['u_id'] != user2_info['u_id']

def test_http_correct_token():
    '''
    Checks if registered users are assigned a unique token
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
        'name_first': 'Lavar',
        'name_last': 'Ball',
    })
    payload1 = r1.json()
    payload2 = r2.json()

    assert payload1['token'] != payload2['token']

def test_http_unique_session_id():
    '''
    Checks if registered users are assigned unique session id's
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
        'name_first': 'Lavar',
        'name_last': 'Ball',
    })
    payload1 = r1.json()
    payload2 = r2.json()

    user1_info = jwt.decode(payload1['token'], SECRET, algorithms=['HS256'])
    user2_info = jwt.decode(payload2['token'], SECRET, algorithms=['HS256'])
    assert user1_info['session_id'] != user2_info['session_id']

def test_http_token_works():
    '''
    Check if generated token matches user id
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    payload1 = r1.json()

    user1_info = jwt.decode(payload1['token'], SECRET, algorithms=['HS256'])
    assert user1_info['u_id'] == payload1['auth_user_id']

def test_http_unique_invalid_email():
    '''
    Check if email entered is invalid
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'bademailcom',
        'password': 'user1password',
        'name_first': '%Kanye@_',
        'name_last': '%Yeezus__!@',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': '',
        'password': 'user2password',
        'name_first': 'Kanye',
        'name_last': 'East',
    })
    r3 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'emaillongerthan254characters' * 40,
        'password': 'user3password',
        'name_first': 'Kanye',
        'name_last': 'South',
    })
    assert r1.status_code == 400
    assert r2.status_code == 400
    assert r3.status_code == 400

def test_http_register_duplicate_email():
    '''
    Check if email address is already being used by another user
    '''
    requests.delete(config.url + 'clear/v1')
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

def test_http_register_password_length():
    '''
    Check if length of password is less than 6 characaters
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'pw',
        'name_first': 'Kanye',
        'name_last': 'Yeezus',
    })
    assert r1.status_code == 400

def test_http_register_fname_length():
    '''
    Check if length of name_first is not between 1 and 50 characters inclusive
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': '',
        'name_last': 'Yeezus',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'ffffff' * 10,
        'name_last': 'Ball',
    })
    assert r1.status_code == 400
    assert r2.status_code == 400

def test_http_register_lname_length():
    '''
    Check if length of name_last is not between 1 and 50 characters inclusive
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'Kanye',
        'name_last': '',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'Lavar',
        'name_last': 'ffffff' * 10,
    })
    assert r1.status_code == 400
    assert r2.status_code == 400

def test_unique_handle():
    '''
    Have to create 3 unique handles with the same name for coverage
    '''
    requests.delete(config.url + 'clear/v1')
    r1 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user1@email.com',
        'password': 'user1password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    r2 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user2@email.com',
        'password': 'user2password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user3@email.com',
        'password': 'user3password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user4@email.com',
        'password': 'user4password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user5@email.com',
        'password': 'user5password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user6@email.com',
        'password': 'user6password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user7@email.com',
        'password': 'user7password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user8@email.com',
        'password': 'user8password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user8@email.com',
        'password': 'user8password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user9@email.com',
        'password': 'user9password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user10@email.com',
        'password': 'user10password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    requests.post(config.url + 'auth/register/v2', json={
        'email': 'user11@email.com',
        'password': 'user11password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    r3 = requests.post(config.url + 'auth/register/v2', json={
        'email': 'user12@email.com',
        'password': 'user12password',
        'name_first': 'KanyeKanyeKanye123',
        'name_last': 'WestWestWest123',
    })
    assert r1.status_code != 400
    assert r2.status_code != 400
    assert r3.status_code != 400