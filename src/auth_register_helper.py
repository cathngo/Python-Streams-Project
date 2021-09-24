#auth_register_v1 helper functions
import re
from src.error import InputError

# Checks user's email to see whether it is valid or not
def check_email(email):
    # Regular expression for validating an email
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    
    # Email length cannot be 0 or greater than 254
    if len(email) == 0 or len(email) > 254:
        raise InputError
    
    # Checks if invalid email format
    if not re.fullmatch(regex, email):
        raise InputError

# Checks if an email address is already being used by another user
def check_duplicate_email(email, store):
    for user in store['users']:
        if user['email'] == email:
            raise InputError

# Checks if user's password less than 6 characters (invalid)
def check_password(password):
    if len(password) < 6:
        raise InputError

# Checks if length of user's first and last name is not between 1 and 50 characters inclusive (invalid)
def check_name(name):
    if len(name) < 1 or len(name) > 50:
        raise InputError

# Check data_store to see if generated handle is already in use
# Return True if handle is already in use, otherwise return False
def check_duplicate_handle(handle_str, store):
    for user in store['users']:
        if user['handle_str'] == handle_str:
            return True
    return False

# Generates a unique handle for the user
def create_handle(name_first, name_last, store):
    # Concatenates lowercase-only alphanumeric (a-z0-9) first name and last name.
    handle_str = ''
    for character in name_first:
        if character.islower() or character.isdigit():
            handle_str += character

    for character in name_last:
        if character.islower() or character.isdigit():
            handle_str += character

    # If length of handle is longer than 20 characters, it is cut off at 20 characters
    if len(handle_str) > 20:
        handle_str = handle_str[:20]

    '''
    If the handle is once again taken, append the concatenated names with the smallest
    number (starting from 0) that forms a new handle that isn't already taken.
    '''
    if check_duplicate_handle(handle_str, store) == True:
        handle_str += '0'

    '''
    If the newly formed handle is already taken, increment the number and append to the handle
    until newly created handle is unique.
    '''
    append_num = 1
    append_num_digits = 1
    while check_duplicate_handle(handle_str, store) == True:
        handle_str = handle_str[:-append_num_digits] + str(append_num)
        if append_num % (10 ** append_num_digits) == 0:
            append_num_digits += 1
        append_num += 1

    return handle_str