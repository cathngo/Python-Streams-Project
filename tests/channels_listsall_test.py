import pytest

from src.error import InputError, AccessError
from src.channels import channels_create_v1, channels_listall_v1
from src.auth import auth_register_v1
from src.other import clear_v1

def test_no_channels():
    clear_v1()
    
    #check when there is no channels
    user_id1 = auth_register_v1('test1@gmail.com', 'test321', 'Jack', 'Smith')
    all_channels = channels_listall_v1(user_id1['auth_user_id'])
    assert len(all_channels['channels']) == 0
    


def test_multiple_channels_listsall():
    clear_v1()
    user_id1 = auth_register_v1('test1@gmail.com', 'test321', 'Jack', 'Smith')
    user_id2 = auth_register_v1('other1@gmail.com', 'test321', 'Willis', 'Posa')
    
    # check multiple public channels with different users
    channels_create_v1(user_id2['auth_user_id'], 'member', True)  
    channels_create_v1(user_id1['auth_user_id'], 'member1', True)
    channels_create_v1(user_id1['auth_user_id'], 'member2', True)
    channels_create_v1(user_id1['auth_user_id'], 'member3', True)
    all_channels = channels_listall_v1(user_id1['auth_user_id'])
    assert len(all_channels['channels']) == 4
    
    
def test_private_channels_list():
    clear_v1()
    user_id1 = auth_register_v1('test1@gmail.com', 'test321', 'Jack', 'Smith')
    user_id2 = auth_register_v1('other1@gmail.com', 'test321', 'Willis', 'Posa')
    
    # check multiple channels including private ones
    channels_create_v1(user_id2['auth_user_id'], 'test1', True)  
    channels_create_v1(user_id1['auth_user_id'], 'test2', True)
    channels_create_v1(user_id2['auth_user_id'], 'test3', False)
    channels_create_v1(user_id1['auth_user_id'], 'test4', False)
    all_channels = channels_listall_v1(user_id1['auth_user_id'])
    assert len(all_channels['channels']) == 4
    
