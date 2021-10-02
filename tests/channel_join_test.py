import pytest

from src.error import InputError, AccessError
from src.channels import channels_create_v1
from src.channel import channel_details_v1, channel_join_v1
from src.auth import auth_register_v1
from src.other import clear_v1

#user id data
@pytest.fixture
def u_id():
    clear_v1()
    return auth_register_v1('valid@gmail.com', 'abcde123*', 'Snoop', 'Dogg')

#channel id data
@pytest.fixture
def c_id(u_id):
    return channels_create_v1(u_id['auth_user_id'], 'Rappers', True)  

# Checks if channel exists in channel list
def test_invalid_channel_id(u_id):
    invalid_channel_id = 124
    with pytest.raises(InputError):
        channel_join_v1(u_id['auth_user_id'], invalid_channel_id)
        
# Checks if channel exists in channel list
def test_invalid_channel_id2(u_id, c_id):
    invalid_channel_id = c_id['channel_id'] + 1
    with pytest.raises(InputError):
        channel_join_v1(u_id['auth_user_id'], invalid_channel_id)

# Checks to see if user is already a member of the channel
def test_existing_member(u_id, c_id):
    u_id2 = auth_register_v1('valid2@gmail.com', 'abcdef123*', 'Kanye', 'Dogg')
    channel_join_v1(u_id2['auth_user_id'], c_id['channel_id'])
    with pytest.raises(InputError):
        channel_join_v1(u_id2['auth_user_id'], c_id['channel_id'])

# If channel is private and user is not global owner check if join is prevented
def test_invalid_private_join(u_id):
    c_id = channels_create_v1(u_id['auth_user_id'], 'Rappers', False) 
    u_id2 = auth_register_v1('valid2@gmail.com', 'abcdef123*', 'Drake', 'Dogg')
    with pytest.raises(AccessError):
        channel_join_v1(u_id2['auth_user_id'], c_id['channel_id'])

# Check if new member has been added to the member list
def test_member_update(u_id, c_id):
    u_id2 = auth_register_v1('valid2@gmail.com', 'abcdef123*', 'Drake', 'Dogg')
    channel_join_v1(u_id2['auth_user_id'], c_id['channel_id'])
    details = channel_details_v1(u_id['auth_user_id'], c_id['channel_id']) 
    assert len(details['all_members']) == 2
    
    
    
    
    
    
