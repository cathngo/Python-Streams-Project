from src.data_store import data_store
from src.data_persistence import save_pickle, open_pickle
import smtplib
import hashlib
import random
import string

def send_email_to_reset(email):
    '''
    Given an email, send an unique code to change the password.

    Arguments:
        email (string) - the email of the account that wants to reset the password
    Exceptions:
        None
    Return Value: 
        None
    '''
    store = open_pickle()
    #create a random string size 15 
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(15))
    hashed_code = hashlib.sha256(result_str.encode()).hexdigest()
    #find the user and stores the hashed code 
    for user in store['users']:
        if user['email'] == email and len(user['session_list']) == 0:
            user['password_reset'] = hashed_code
            break
    else:
        return

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        sender =  "alpacareseter@gmail.com"
        receiver =  email
        password = "alpaquita"
        subject = 'password code'
        body = f'Use the following code to reset your password: {result_str}'
        msg = f'Subject: {subject}\nTo: {email}\n\n{body}'
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg)
        smtp.quit()
    
    data_store.set(store)
    save_pickle()