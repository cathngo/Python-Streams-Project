import urllib.request
from PIL import Image
from src.error import InputError
from flask import current_app
import os

def check_valid_coordinates(img, x_start, y_start, x_end, y_end, auth_user_id):
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
    if x_end < x_start or y_end < y_start:
        os.remove(os.path.join(current_app.root_path, 'images/') + str(auth_user_id) + ".jpg")
        raise InputError(description="x end value larger than x start value")
        
    #check if y_end less than y_start
    if y_end < y_start:
        os.remove(os.path.join(current_app.root_path, 'images/') + str(auth_user_id) + ".jpg")
        raise InputError(description="y end value larger than y start value")

def download_image(img_url, auth_user_id):
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
    #raise input error if not jpg or jpeg
    img = Image.open(img)

    if img.format != 'JPEG' and img.format != 'JPG':
        #remove the downloaded image
        os.remove(os.path.join(current_app.root_path, 'images/') + str(auth_user_id) + ".jpg")
        raise InputError(description="not valid format " + str(img.format))


def crop_image(img, x_start, y_start, x_end, y_end):
    imageObject = Image.open(img)
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(img)
