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
    with pytest.raises(InputError):
        channel_details_v1(u_id['auth_user_id'],5)
    #channels exist, but given wrong channel id
    c_id = channels_create_v1(id['auth_user_id'], 'Alpaca', True) 
    invalid_channel_id = c_id['channel_id'] + 1
    with pytest.raises(InputError):
        channel_details_v1(id['auth_user_id'],invalid_channel_id)

#check channel id valid but auth id invalid
def test_unauthorised_member():
    clear_v1()
    #check empty u_id
    id_zero = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    c_id = channels_create_v1(id_zero['auth_user_id'], 'Alpaca', True) 
    invalid_u_id = id_zero['auth_user_id'] + 1
    with pytest.raises(AccessError):
        channel_details_v1(invalid_u_id,c_id['channel_id'])  

#check empty data
def test_empty_store():
    clear_v1()
    with pytest.raises(InputError):
        channel_details_v1(0,0)

#check returns correct details for given channel
def test_correct_details():
    clear_v1()
    u_id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    c_id = channels_create_v1(u_id['auth_user_id'], 'Alpaca', True) 
    details = channel_details_v1(u_id['auth_user_id'],c_id['channel_id'])
    assert details['name'] == 'Alpaca'
    assert details['is_public'] == True
    assert details['owner_members'][0]['u_id'] == u_id['u_id']
    assert details['all_members'][0]['u_id'] == c_id['channel_id']

#check returns correct channel details given multiple channels a user has created
def test_multiple_channels():
    clear_v1()
    u_id_zero = auth_register_v1('emailzero@gmail.com', '123abc!@#', 'Sam', 'Smith')
    c_id_zero = channels_create_v1(u_id_zero['auth_user_id'], 'Channel Zero', True) 
    c_id_one = channels_create_v1(u_id_zero['auth_user_id'], 'Channel One', True) 
    c_id_two =channels_create_v1(u_id_zero['auth_user_id'], 'Channel Two', True) 
    details = channel_details_v1(u_id_zero['auth_user_id'], c_id_two['channel_id'])
    assert details['name'] == 'Channel Two'
    assert details['is_public'] == True
    assert details['owner_members'][0]['u_id'] == u_id_zero['u_id']
    assert details['all_members'][0]['u_id'] == c_id_two['channel_id']


    
   