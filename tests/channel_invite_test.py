import pytest

from src.error    import InputError, AccessError
from src.channels import channels_create_v1, channels_list_v1
from src.auth     import auth_register_v1
from src.channel  import channel_invite_v1
from src.other    import clear_v1

@pytest.fixture
def clear_register_create_channel():
    clear_v1()
    #register user
    user_id1 = auth_register_v1('test1@gmail.com', 'testing1', 'Jack', 'Smith')
    #create a channel
    channel_id1 = channels_create_v1(user_id1['auth_user_id'], 'channel1', True)
    return [user_id1['auth_user_id'], channel_id1['channel_id']]

def test_invite_invalid_u_id(clear_register_create_channel):
    ids_list = clear_register_create_channel
    user_id = ids_list[0]
    channel_id = ids_list[1]
    invalid_user = 404
    with pytest.raises(InputError):
        channel_invite_v1(user_id, channel_id, invalid_user)
        
def test_invite_to_invalid_channel(clear_register_create_channel):
    ids_list = clear_register_create_channel
    user_id = ids_list[0]
    invalid = 404
    user_id2 = auth_register_v1('test2@gmail.com', 'testing1', 'Willy', 'Masko')
    
    with pytest.raises(InputError):
        channel_invite_v1(user_id, invalid, user_id2['auth_user_id'])
        
def test_invite_already_member(clear_register_create_channel):
    ids_list = clear_register_create_channel
    user_id = ids_list[0]
    channel_id = ids_list[1]
    user_id2 = auth_register_v1('test2@gmail.com', 'testing1',  'Willy', 'Masko')
    
    channel_invite_v1(user_id, channel_id, user_id2['auth_user_id'])
    with pytest.raises(InputError):
        channel_invite_v1(user_id, channel_id, user_id2['auth_user_id'])

def test_unauthorised_invitation(clear_register_create_channel):
    ids_list = clear_register_create_channel
    user_id = ids_list[0]
    channel_id = ids_list[1]
    user_id2 = auth_register_v1('test2@gmail.com', 'testing2', 'Willy', 'Masko')
    user_id3 = auth_register_v1('test3@gmail.com', 'testing3', 'Putem', 'Rodri')
    #invite an user when the inviter is not the owner
    with pytest.raises(AccessError):
        channel_invite_v1(user_id2['auth_user_id'],
                         channel_id, user_id3['auth_user_id'])

def test_invite_u_id(clear_register_create_channel):
    ids_list = clear_register_create_channel
    user_id = ids_list[0]
    channel_id = ids_list[1]
    user_id2 = auth_register_v1('test2@gmail.com', 'testing2', 'Willy', 'Masko')
    channel_invite_v1(user_id, channel_id, user_id2['auth_user_id'])
    list1 = channels_list_v1(user_id)
    list2 = channels_list_v1(user_id2['auth_user_id'])
    assert list1 == list2

def test_invited_user_invites(clear_register_create_channel):
    ids_list = clear_register_create_channel
    user_id = ids_list[0]
    channel_id = ids_list[1]
    user_id2 = auth_register_v1('test2@gmail.com', 'testing2', 'Willy', 'Masko')
    user_id3 = auth_register_v1('test3@gmail.com', 'testing3', 'Putem', 'Rodri')
    channel_invite_v1(user_id, channel_id, user_id2['auth_user_id'])
    channel_invite_v1(user_id2['auth_user_id'],
                     channel_id, user_id3['auth_user_id'])
    list1 = channels_list_v1(user_id)
    list2 = channels_list_v1(user_id2['auth_user_id'])
    list3 = channels_list_v1(user_id3['auth_user_id'])
    assert list1 == list2
    assert list2 == list3
