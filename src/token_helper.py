import jwt
from src.error import AccessError
from src.data_store import data_store
from src.config import SECRET

def decode_jwt(encoded_jwt):
    return jwt.decode(encoded_jwt, SECRET, algorithms=['HS256'])

def check_valid_token(user_token):
    store = data_store.get()

    for user in store['users']:
        if user['u_id'] == user_token['u_id'] and user_token['session_id'] in user['session_list']:
            return
    raise AccessError("Invalid token - no user associated") 
    
