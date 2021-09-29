import pytest

from src.error import InputError, AccessError
from src.channels import channels_create_v1
from src.channel import channel_details_v1
from src.auth import auth_register_v1
from src.other import clear_v1

#check channel id exists
def test_nonexistent_channel_id():
    clear_v1()
    #no channels
    u_id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    invalid_channel_id = 100
    with pytest.raises(InputError):
        channel_details_v1(u_id['auth_user_id'], invalid_channel_id)

#channels exist, but given wrong channel id
def test_invalid_channel_id():
    clear_v1()
    u_id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    c_id = channels_create_v1(u_id['auth_user_id'], 'Alpaca', True) 
    invalid_channel_id = c_id['channel_id'] + 1
    with pytest.raises(InputError):
        channel_details_v1(u_id['auth_user_id'], invalid_channel_id)

#check channel id valid but auth id invalid
def test_unauthorised_member():
    clear_v1()
    id_zero = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    c_id = channels_create_v1(id_zero['auth_user_id'], 'Alpaca', True) 
    invalid_u_id = id_zero['auth_user_id'] + 1
    with pytest.raises(AccessError):
        channel_details_v1(invalid_u_id, c_id['channel_id'])  

#check empty data
def test_empty_store():
    clear_v1()
    with pytest.raises(AccessError):
        channel_details_v1(0, 0)

#check returns correct owner details of given channel
def test_correct_owner_details():
    clear_v1()
    u_id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    c_id = channels_create_v1(u_id['auth_user_id'], 'Alpaca', True) 
    details = channel_details_v1(u_id['auth_user_id'], c_id['channel_id']) 
    assert details['owner_members'][0]['u_id'] == u_id['auth_user_id']
    assert details['owner_members'][0]['email'] == 'validemail@gmail.com'
    assert details['owner_members'][0]['name_first'] == 'Sam'
    assert details['owner_members'][0]['name_last'] == 'Smith'

#check returns correct member details of given channel
def test_correct_member_details():
    clear_v1()
    u_id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    c_id = channels_create_v1(u_id['auth_user_id'], 'Alpaca', True) 
    details = channel_details_v1(u_id['auth_user_id'], c_id['channel_id']) 
    assert details['all_members'][0]['u_id'] == u_id['auth_user_id']
    assert details['all_members'][0]['email'] == 'validemail@gmail.com'
    assert details['all_members'][0]['name_first'] == 'Sam'
    assert details['all_members'][0]['name_last'] == 'Smith'

#check returns correct name and is_public details
def test_correct_channel_details():
    clear_v1()
    u_id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    c_id = channels_create_v1(u_id['auth_user_id'], 'Alpaca', False) 
    details = channel_details_v1(u_id['auth_user_id'], c_id['channel_id']) 
    assert details['name'] == 'Alpaca'
    assert details['is_public'] == False

#check returns correct channel details given multiple channels a user has created
def test_multiple_channels():
    clear_v1()
    #register first user
    u_id_zero = auth_register_v1('emailzero@gmail.com', '123abc!@#', 'Sam', 'Smith')
    #create multiple channels with first user
    c_id_zero = channels_create_v1(u_id_zero['auth_user_id'], 'Channel Zero', True) 
    c_id_one = channels_create_v1(u_id_zero['auth_user_id'], 'Channel One', False) 
    c_id_two = channels_create_v1(u_id_zero['auth_user_id'], 'Channel Two', True) 
    #test details of channel two is correct
    details = channel_details_v1(u_id_zero['auth_user_id'], c_id_two['channel_id'])
    assert details['name'] == 'Channel Two'
    