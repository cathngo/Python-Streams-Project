import pytest

from src.error import InputError, AccessError
from src.channels import channels_create_v1
from src.channel import channel_details_v1
from src.auth import auth_register_v1
from src.other import clear_v1

#user id data
@pytest.fixture
def test_u_id():
    clear_v1()
    return auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')

#channel id data
@pytest.fixture
def test_c_id(test_u_id):
    return channels_create_v1(test_u_id['auth_user_id'], 'Alpaca', True) 

#check when no channels created
def test_nonexistent_channel_id(test_u_id):
    invalid_channel_id = 1000
    with pytest.raises(InputError):
        channel_details_v1(test_u_id['auth_user_id'], invalid_channel_id)

#channels exist, but given wrong channel id
def test_invalid_channel_id(test_u_id, test_c_id):
    invalid_channel_id = test_c_id['channel_id'] + 1
    with pytest.raises(InputError):
        channel_details_v1(test_u_id['auth_user_id'], invalid_channel_id)

#check channel id valid but auth id is not part of channel
def test_unauthorised_member(test_u_id, test_c_id):
    invalid_u_id = test_u_id['auth_user_id'] + 1
    with pytest.raises(AccessError):
        channel_details_v1(invalid_u_id, test_c_id['channel_id'])  

#check when both channel id and auth id invalid
def test_empty_store():
    clear_v1()
    with pytest.raises(AccessError):
        channel_details_v1(0, 0)

#check returns correct owner details of given channel
def test_correct_owner_details(test_u_id, test_c_id):
    details = channel_details_v1(test_u_id['auth_user_id'], test_c_id['channel_id']) 
    assert details['owner_members'][0]['u_id'] == test_u_id['auth_user_id']
    assert details['owner_members'][0]['email'] == 'validemail@gmail.com'
    assert details['owner_members'][0]['name_first'] == 'Sam'
    assert details['owner_members'][0]['name_last'] == 'Smith'

#check returns correct member details of given channel
def test_correct_member_details(test_u_id, test_c_id):
    details = channel_details_v1(test_u_id['auth_user_id'], test_c_id['channel_id']) 
    assert details['all_members'][0]['u_id'] == test_u_id['auth_user_id']
    assert details['all_members'][0]['email'] == 'validemail@gmail.com'
    assert details['all_members'][0]['name_first'] == 'Sam'
    assert details['all_members'][0]['name_last'] == 'Smith'

#check returns correct name and is_public details
def test_correct_channel_details(test_u_id, test_c_id):
    details = channel_details_v1(test_u_id['auth_user_id'], test_c_id['channel_id']) 
    assert details['name'] == 'Alpaca'
    assert details['is_public'] == True

#check returns correct channel details given multiple channels a user has created
def test_multiple_channels(test_u_id):
    #create multiple channels with first user
    channels_create_v1(test_u_id['auth_user_id'], 'Channel Zero', True) 
    channels_create_v1(test_u_id['auth_user_id'], 'Channel One', True) 
    c_id_two = channels_create_v1(test_u_id['auth_user_id'], 'Channel Two', False) 
    #test returns details of channel two
    details = channel_details_v1(test_u_id['auth_user_id'], c_id_two['channel_id'])
    assert details['name'] == 'Channel Two'
    assert details['is_public'] == False
