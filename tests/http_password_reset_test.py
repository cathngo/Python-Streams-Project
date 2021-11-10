import requests
from src import config
from src.error import InputError, AccessError
from tests.pytest_fixtures import clear, reg_user_alpaca, reg_user2, reg_user1

def test_invalid_code(clear, reg_user_alpaca):
    reg_user_alpaca
    re = requests.post(config.url + 'auth/passwordreset/reset/v1', json={'reset_code': 'invalid_code','new_password': 'validpassword'})
    assert re.status_code == InputError.code

def test_invalid_password(clear, reg_user1):
    reg_user1
    re = requests.post(config.url + 'auth/passwordreset/reset/v1', json={'reset_code': 'invalid_code','new_password': 'inval'})
    assert re.status_code == InputError.code




