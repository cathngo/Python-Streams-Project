import pytest

from src.error import InputError, AccessError
from src.channels import channels_create_v1
from src.channel import channel_details_v1
from src.auth import auth_register_v1
from src.other import clear_v1

#test data for user id
@pytest.fixture
def test_u_id():
    clear_v1()
    return auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')

#check function returns channel id
def test_returns_channel_id(test_u_id):
    c_id = channels_create_v1(test_u_id['auth_user_id'], 'Alpaca', False)
    assert len(c_id) != 0

#check if name is less than 1 character or greater than 20 characters
def test_channels_invalid_name(test_u_id):
    with pytest.raises(InputError):
        channels_create_v1(test_u_id['auth_user_id'], '', True)      
    with pytest.raises(InputError):
        channels_create_v1(test_u_id['auth_user_id'], 'nameLongerThanTwentyCharacters', True) 
         
#check auth_id exists
def test_nonexistent_auth_id(test_u_id):
    #check empty database
    invalid_auth_id = 10000
    with pytest.raises(AccessError):
        channels_create_v1(invalid_auth_id, 'channel_name', True)
    #check empty u_id
    invalid_u_id = test_u_id['auth_user_id'] + 1
    with pytest.raises(AccessError):
        channels_create_v1(invalid_u_id, 'channel_name', True)  
       
#check channel id is unique
def test_unique_channel_id(test_u_id):
    channel_id_one = channels_create_v1(test_u_id['auth_user_id'], 'channel_one', True)
    channel_id_two = channels_create_v1(test_u_id['auth_user_id'], 'channel_two', True)
    assert channel_id_one != channel_id_two

#check creator of channel is the owner
def test_owner(test_u_id):
    c_id = channels_create_v1(test_u_id['auth_user_id'], 'Alpaca', False)
    details = channel_details_v1(test_u_id['auth_user_id'], c_id['channel_id'])
    assert details['owner_members'][0]['u_id'] == test_u_id['auth_user_id']
    assert details['all_members'][0]['u_id'] == test_u_id['auth_user_id']  

#check name is added
def test_channel_name(test_u_id):
    c_id = channels_create_v1(test_u_id['auth_user_id'], 'Alpaca', False)
    details = channel_details_v1(test_u_id['auth_user_id'], c_id['channel_id'])
    assert details['name'] == 'Alpaca'

#check correct is_public value added
def test_is_public(test_u_id):
    c_id = channels_create_v1(test_u_id['auth_user_id'], 'Alpaca', False)
    details = channel_details_v1(test_u_id['auth_user_id'], c_id['channel_id'])
    assert details['is_public'] == False
