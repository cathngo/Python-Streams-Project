import urllib.request
from PIL import Image
from src.error import InputError
from flask import current_app
import os

def check_valid_coordinates(img, x_start, y_start, x_end, y_end):
    imageObject = Image.open(img)
    
    #check coordinates within img dimensions
    if x_start < 0 or x_start > imageObject.width:
        raise InputError(description="value not within width of image of" + str(imageObject.width) + img)
      
    if y_start < 0 or y_start > imageObject.height:
        raise InputError(description="value not within height of image of "+ str(imageObject.height))

    #check if x_end less than x_start/y_end less than y_start
    if x_end < x_start or y_end < y_start:
        raise InputError(description="end value larger than start value")

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

def check_valid_format(img):
    #raise input error if not jpg or jpeg
    img = Image.open(img)

    if img.format != 'JPEG' and img.format != 'JPG':
        raise InputError(description="not valid format " + str(img.format))

def crop_image(img, x_start, y_start, x_end, y_end):
    imageObject = Image.open(img)
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(img)
    #save to datastore
