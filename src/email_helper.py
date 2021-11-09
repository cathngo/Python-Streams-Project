from src.error import InputError, AccessError
from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
import smtplib
import hashlib
import random
import string
from email.message import EmailMessage

def send_email_to_reset(email):
    store = open_pickle()
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(15))
    hashed_code = hashlib.sha256(result_str.encode()).hexdigest()
    
    for user in store['users']:
        if user['email'] == email and len(user['session_list']) == 0:
            user['password_reset'] = hashed_code
            break
    else:
        return

    sender =  "alpacareseter@gmail.com"
    reciber =  "alpacatesting123@gmail.com"
    password = "alpaquita"
    message = f"Use the following code to reset your password: {result_str}"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendemail(sender,reciber,message)

    
    data_store.set(store)
    save_pickle()