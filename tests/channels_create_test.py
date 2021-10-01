import pytest

from src.error import InputError, AccessError
from src.channels import channels_create_v1
from src.auth import auth_register_v1
from src.other import clear_v1

#test data for user id
@pytest.fixture
def test_u_id():
    clear_v1()
    return auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')

#check if name is less than 1 character or greater than 20 characters
def test_channels_invalid_name(test_u_id):
    with pytest.raises(InputError):
        channels_create_v1(test_u_id['auth_user_id'], '', True)      
    with pytest.raises(InputError):
        channels_create_v1(test_u_id['auth_user_id'], 'nameLongerThanTwentyCharacters', True) 
         

#check auth_id exists
def test_nonexistent_auth_id(test_u_id):
    #check empty user list
    invalid_channel_id = 10000
    with pytest.raises(AccessError):
        channels_create_v1(invalid_channel_id, 'channel_name', True)
    #check empty u_id
    invalid_u_id = test_u_id['auth_user_id'] + 1
    with pytest.raises(AccessError):
        channels_create_v1(invalid_u_id, 'channel_name', True)  
       
#check channel id is unique
def test_unique_channel_id(test_u_id):
    id_two = auth_register_v1('validemailtwo@gmail.com', '123abc!@', 'Sam', 'Smith')
    channel_id_one = channels_create_v1(test_u_id['auth_user_id'], 'channel_name', True)
    channel_id_two = channels_create_v1(id_two['auth_user_id'], 'channel_name', True)
    assert channel_id_one != channel_id_two
