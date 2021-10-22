import pytest

from src.error import InputError, AccessError
from src.channels import channels_create_v1, channels_list_v1
from src.auth import auth_register_v1
from src.other import clear_v1


@pytest.fixture
def clear_register_create_channels():
    clear_v1()
    #register users
    user_id1 = auth_register_v1('test1@gmail.com', 'test321', 'Jack', 'Smith')
    user_id2 = auth_register_v1('other1@gmail.com', 'test4321', 'Willis', 'Posa')
    #create the channels
    channels_create_v1(user_id1['auth_user_id'], 'is_member1', True)
    channels_create_v1(user_id1['auth_user_id'], 'is_member2', True)
    channels_create_v1(user_id1['auth_user_id'], 'is_member3', True)
    return [user_id1, user_id2]

def test_no_channel_joined():
    clear_v1()
    
    #check when there is no channels
    user_id1 = auth_register_v1('test1@gmail.com', 'test321', 'Jack', 'Smith')
    joined_channels = channels_list_v1(user_id1['auth_user_id'])
    assert len(joined_channels['channels']) == 0
    
def test_no_channel_joined2():
    clear_v1()
    #check when there is other channels
    user_id1 = auth_register_v1('test1@gmail.com', 'test321', 'Jack', 'Smith')
    user_id2 = auth_register_v1('other1@gmail.com', 'test4321', 'Willis', 'Posa')
    channels_create_v1(user_id2['auth_user_id'], 'is_member1', True)
    joined_channels = channels_list_v1(user_id1['auth_user_id'])
    assert len(joined_channels['channels']) == 0
'''
def test_auth_invalid_2():
    clear_v1()
    with pytest.raises(AccessError):
        channels_list_v1(404)
'''     
def test_multiple_channels_list(clear_register_create_channels):
    user_id1 = clear_register_create_channels
    joined_channels = channels_list_v1(user_id1[0]['auth_user_id'])
    assert len(joined_channels['channels']) == 3
    
    
def test_private_channels_list(clear_register_create_channels):
    users = clear_register_create_channels
    # check when user_id1 is member in multiple channels including private ones
    channels_create_v1(users[0]['auth_user_id'], 'is_member4', False)
    joined_channels = channels_list_v1(users[0]['auth_user_id'])
    assert len(joined_channels['channels']) == 4
