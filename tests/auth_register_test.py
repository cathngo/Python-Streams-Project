# import pytest

# from src.auth import auth_register_v1, auth_login_v1
# from src.error import InputError
# from src.other import clear_v1

# # Check if email entered is invalid
# def test_register_invalid_email():
#     clear_v1()
#     with pytest.raises(InputError):
#         auth_register_v1('bademail.com', 'password', 'firstname', 'lastname')
#     with pytest.raises(InputError):
#         auth_register_v1('', 'password', 'firstname', 'lastname')

# # Check if email address is already being used by another user
# def test_register_duplicate_email():
#     clear_v1()
#     auth_register_v1('user@email.com', 'password', 'firstname', 'lastname')
#     with pytest.raises(InputError):
#         auth_register_v1('user@email.com', 'password', 'firstname', 'lastname')

# # Check if length of password is less than 6 characaters
# def test_register_password_length():
#     clear_v1()
#     with pytest.raises(InputError):
#         auth_register_v1('user@email.com', 'asd', 'firstname', 'lastname')

# # Check if length of name_first is not between 1 and 50 characters inclusive
# def test_register_fname_length():
#     clear_v1()
#     with pytest.raises(InputError):
#         auth_register_v1('user@email.com', 'password', '', 'lastname')
#     with pytest.raises(InputError):
#         auth_register_v1('user@email.com', 'password', 'ffffff' * 10, 'lastname')

# # Check if length of name_last is not between 1 and 50 characters inclusive
# def test_register_lname_length():
#     clear_v1()
#     with pytest.raises(InputError):
#         auth_register_v1('user@email.com', 'password', 'firstname', '')
#     with pytest.raises(InputError):
#         auth_register_v1('user@email.com', 'password', 'firstname', 'llllll' * 10)

# # Check if 2 registered users are given unique ids
# def test_register_unique_id():
#     clear_v1()
#     auth_user1_id = auth_register_v1('user1@email.com', 'password', 'Bob', 'lastname')
#     auth_user2_id = auth_register_v1('user2@email.com', 'password', 'John', 'lastname')
#     assert auth_user1_id != auth_user2_id

# # # Check if user id generated from auth_register matches returned id from auth_login
# # def test_register_works():
# #     clear_v1()
# #     user_return = auth_register_v1('user@email.com', 'password', 'firstname', 'lastname')
# #     user_id = user_return['auth_user_id']

# #     user_login_return = auth_login_v1('user@email.com', 'password')
# #     login_id = user_login_return['auth_user_id']
# #     assert user_id == login_id