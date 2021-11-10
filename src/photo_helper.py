import urllib.request
from PIL import Image
from src.error import InputError
from flask import current_app
import os
from src.data_persistence import save_pickle, open_pickle
from src.data_store import data_store
from src import config

def check_valid_coordinates(img, x_start, y_start, x_end, y_end, auth_user_id):
    '''
Checks if any of the coordinates given are valid

Arguments:
    img (String) - the path to the downloaded image
    x_start (int) - the start position on the x axis to crop the image
    y_start (int) - the start position on the y axis to crop the image
    x_end (int) - the end position on the x axis to crop the image
    y_end (int) - the end position on the y axis to crop the image
    auth_user_id (int) - the id of the user who is uploading the photo

Exceptions:
    InputError - Occurs when any of:
        - any of x_start, y_start, x_end, y_end are not within the dimensions of the image at the URL
        - x_end is less than x_start or y_end is less than y_start

Return Value: 
    Returns void upon success
'''
    imageObject = Image.open(img)
    
    #check coordinates within img dimensions
    if x_start < 0 or x_start > imageObject.width:
        os.remove(os.path.join(current_app.root_path, 'images/') + str(auth_user_id) + ".jpg")
        raise InputError(description="value not within width of image")
        
    if x_end < 0 or x_end > imageObject.width:
        os.remove(os.path.join(current_app.root_path, 'images/') + str(auth_user_id) + ".jpg")
        raise InputError(description="value not within width of image")  

    if y_start < 0 or y_start > imageObject.height:
        os.remove(os.path.join(current_app.root_path, 'images/') + str(auth_user_id) + ".jpg")
        raise InputError(description="value not within height of image")

    if y_end < 0 or y_end > imageObject.height:
        os.remove(os.path.join(current_app.root_path, 'images/') + str(auth_user_id) + ".jpg")
        raise InputError(description="value not within height of image")

    #check if x_end less than x_start
    if x_end < x_start:
        os.remove(os.path.join(current_app.root_path, 'images/') + str(auth_user_id) + ".jpg")
        raise InputError(description="x end value larger than x start value")
        
    #check if y_end less than y_start
    if y_end < y_start:
        os.remove(os.path.join(current_app.root_path, 'images/') + str(auth_user_id) + ".jpg")
        raise InputError(description="y end value larger than y start value")

def download_image(img_url, auth_user_id):
    '''
Downloads the image given an url to the image into a static folder

Arguments:
    img_url (String) - the url to the image the user wishes to upload
    auth_user_id (int) - the id of the user who is uploading the photo

Exceptions:
    InputError - Occurs when any of:
        - img_url returns an HTTP status other than 200

Return Value: 
    Returns the path to the downloaded image
'''
    #raise input error if not a valid image url
    success = True
    try:
        urllib.request.urlretrieve(img_url, os.path.join(current_app.root_path, 'images/') + str(auth_user_id) + ".jpg")
    except:
        success = False
    if success == False:
        raise InputError(description="not a valid image url")

    return os.path.join(current_app.root_path, 'images/') + str(auth_user_id) + ".jpg"

def check_valid_format(img, auth_user_id):
    '''
Checks if the image is jpg or jpeg

Arguments:
    img (String) - the path to the downloaded image
    auth_user_id (int) - the id of the user who is uploading the photo

Exceptions:
    InputError - Occurs when any of:
        - image uploaded is not a JPG

Return Value: 
    Returns void upon success
'''
    #raise input error if not jpg or jpeg
    img = Image.open(img)

    if img.format != 'JPEG' and img.format != 'JPG':
        #remove the downloaded image
        os.remove(os.path.join(current_app.root_path, 'images/') + str(auth_user_id) + ".jpg")
        raise InputError(description="not valid format " + str(img.format))


def crop_image(img, x_start, y_start, x_end, y_end, user_id):
    '''
Crops the image within the given the boundaries

Arguments:
    img (String) - the path to the downloaded image
    x_start (int) - the start position on the x axis to crop the image
    y_start (int) - the start position on the y axis to crop the image
    x_end (int) - the end position on the x axis to crop the image
    y_end (int) - the end position on the y axis to crop the image
    user_id (int) - the id of the user who is uploading the photo

Return Value: 
    Returns void upon success
'''
    imageObject = Image.open(img)
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(img)
    #save the image to the user's profile
    store = open_pickle()

    for user in store['users']:
        if user['u_id'] == user_id:
            user['profile_img_url'] = config.url + 'static/' + str(user_id) + '.jpg'

    data_store.set(store)
    save_pickle()




