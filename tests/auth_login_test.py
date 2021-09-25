import pytest

from src.auth import auth_login_v1, auth_register_v1
#from src.auth_register_helper import auth_register_helper
from src.error import InputError
from src.other import clear_v1

# Check if email entered does not belong to a user 
def test_incorrect_email():
    with pytest.raises(InputError):
        auth_login_v1('fake@gmail.com','password')

# Check if email entered is not a valid email 
def test_valid_email():
    clear_v1()
    with pytest.raises(InputError):
        auth_login_v1('bademail.com', 'password')
    with pytest.raises(InputError):
        auth_login_v1('','password')
        
# Check if password is not correct 
def test_incorrect_password():
    clear_v1()
    auth_register_v1('diwa@gmail.com','password','diwa','big')
    with pytest.raises(InputError):
        auth_login_v1('diwa@gmail.com', 'wrong')
