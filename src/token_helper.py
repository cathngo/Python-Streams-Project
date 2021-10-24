import jwt
from src.error import AccessError
from src.data_store import data_store
from src.config import SECRET
from src.data_persistence import save_pickle, open_pickle
def decode_jwt(encoded_jwt):
    success = True
    try:
        token = jwt.decode(encoded_jwt, SECRET, algorithms=['HS256'])
    except:
        success = False
    if success == False:
        raise AccessError(description='Could not decode token')
    return token
        
    

def check_valid_token(user_token):
    store = open_pickle()

    for user in store['users']:
        if user['u_id'] == user_token['u_id'] and user_token['session_id'] in user['session_list']:
            return
    raise AccessError(description='Invalid token - no user associated') 
