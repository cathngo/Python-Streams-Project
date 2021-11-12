import requests
from src import config

from tests.pytest_fixtures import clear, reg_user_alpaca, reg_user2

def test_logged_user(clear, reg_user_alpaca):
    re = requests.post(config.url + 'auth/passwordreset/request/v1', json={'email': 'alpacatesting123@gmail.com'})
    assert re.status_code == 200

def test_send_email(clear):
    re = requests.post(config.url + 'auth/passwordreset/request/v1', json={'email': 'invalidemail@gmail.com'})
    assert re.status_code == 200

def test_logged_out(clear, reg_user_alpaca):
    user1 = reg_user_alpaca
    requests.post(config.url + 'auth/logout/v1', json={'token': user1['token']})
    re = requests.post(config.url + 'auth/passwordreset/request/v1', json={'email': 'alpacatesting123@gmail.com'})
    assert re.status_code == 200


