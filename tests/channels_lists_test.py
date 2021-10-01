import pytest

from src.error import InputError, AccessError
from src.channels import channels_create_v1, channels_list_v1
from src.auth import auth_register_v1
from src.other import clear_v1

def test_no_channel_joined():
    clear_v1()
    
    #check when there is no channels
    user_id1 = auth_register_v1('test1@gmail.com', 'test321', 'Jack', 'Smith')
    joined_channels = channels_list_v1(user_id1['auth_user_id'])
    assert len(joined_channels['channels']) == 0
    
    #check when there is other channels
    user_id2 = auth_register_v1('other1@gmail.com', 'test321', 'Willis', 'Posa')
    channels_create_v1(user_id2['auth_user_id'], 'channel1', True)  
    channels_create_v1(user_id2['auth_user_id'], 'channel2', True)
    joined_channels = channels_list_v1(user_id1['auth_user_id'])
    assert len(joined_channels['channels']) == 0

def test_auth_invalid_2():
    clear_v1()
    with pytest.raises(AccessError):
        channels_listall_v1('non_existent')
        
def test_multiple_channels_list():
    clear_v1()
    user_id1 = auth_register_v1('test1@gmail.com', 'test321', 'Jack', 'Smith')
    user_id2 = auth_register_v1('other1@gmail.com', 'test321', 'Willis', 'Posa')
    
    # check when user_id1 is member in multiple channels
    channels_create_v1(user_id2['auth_user_id'], 'is_not_a_member', True)  
    channels_create_v1(user_id1['auth_user_id'], 'is_member1', True)
    channels_create_v1(user_id1['auth_user_id'], 'is_member2', True)
    channels_create_v1(user_id1['auth_user_id'], 'is_member3', True)
    joined_channels = channels_list_v1(user_id1['auth_user_id'])
    assert len(joined_channels['channels']) == 3
    
    
def test_private_channels_list():
    clear_v1()
    user_id1 = auth_register_v1('test1@gmail.com', 'test321', 'Jack', 'Smith')
    user_id2 = auth_register_v1('other1@gmail.com', 'test321', 'Willis', 'Posa')
    
    # check when user_id1 is member in multiple channels including private ones
    channels_create_v1(user_id2['auth_user_id'], 'is_not_a_member', True)  
    channels_create_v1(user_id1['auth_user_id'], 'is_member1', True)
    channels_create_v1(user_id1['auth_user_id'], 'is_member2', False)
    channels_create_v1(user_id1['auth_user_id'], 'is_member3', False)
    joined_channels = channels_list_v1(user_id1['auth_user_id'])
    assert len(joined_channels['channels']) == 1
    
