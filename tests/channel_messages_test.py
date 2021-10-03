import pytest

from src.channel import channel_messages_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.error import InputError, AccessError
from src.channel import channel_messages_v1
from src.auth import auth_register_v1

@pytest.fixture
def clear():
    clear_v1()
    
#check channel id exists
def test_nonexistent_channel_id(clear):
    #no channels
    u_id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    invalid_channel_id = 100
    start = 0
    with pytest.raises(InputError):
        channel_messages_v1(u_id['auth_user_id'],invalid_channel_id, start )
        
#channels exist, but given wrong channel id
def test_invalid_channel_id(clear):
    u_id = auth_register_v1('validemail1@gmail.com', '123abc!@#', 'Sam', 'Smith')
    c_id = channels_create_v1(u_id['auth_user_id'], 'Alpaca', True) 
    invalid_channel_id = c_id['channel_id'] + 1
    start = 0
    with pytest.raises(InputError):
        channel_messages_v1(u_id['auth_user_id'], invalid_channel_id, start)    

#edge case of both channel and user being invalid
def test_invalid_channel_and_user(clear): 
    id_zero = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    invalid_u_id = id_zero['auth_user_id'] + 1
    channel_id = channels_create_v1(id_zero['auth_user_id'], 'Alpaca', True)
    invalid_channel_id = channel_id['channel_id'] + 1
    start = 123
    with pytest.raises(AccessError):
        channel_messages_v1(invalid_u_id, invalid_channel_id, start)

#tests unauthorised users    
def test_unauthorised_member(clear):
    id_zero = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    c_id = channels_create_v1(id_zero['auth_user_id'], 'Alpaca', True) 
    invalid_u_id = id_zero['auth_user_id'] + 1
    start = 0
    with pytest.raises(AccessError):
        channel_messages_v1(invalid_u_id, c_id['channel_id'], start)    

#tests that there is a negative one when the end of a message is reached
def test_negative_one_end_of_messages(clear):
    u_id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    c_id = channels_create_v1(u_id['auth_user_id'], 'Alpaca', True)
    start = 0
    m_id = channel_messages_v1(u_id['auth_user_id'], c_id['channel_id'], 0)  
    assert m_id['end'] == -1  

#start cannot be larger than the messages in the dictionary, otherwise it is an access error
def test_start_greater_than_messages(clear):
    u_id = auth_register_v1('validemail@gmail.com', '123abc!@#', 'Sam', 'Smith')
    c_id = channels_create_v1(u_id['auth_user_id'], 'Alpaca', True) 
    with pytest.raises(InputError):    
        channel_messages_v1(u_id['auth_user_id'], c_id['channel_id'], 1)

