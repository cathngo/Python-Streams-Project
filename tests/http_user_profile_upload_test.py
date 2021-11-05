import pytest
import requests
import json
from src import config
import jwt
from src.error import AccessError, InputError

def test_success():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #register user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #upload photo
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
        'token': user_token['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100,
    })
    assert resp.status_code == 200

def test_invalid_url():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #register user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #upload photo
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
        'token': user_token['token'],
        'img_url': 'http://hello.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100,
    })
    assert resp.status_code == 400

def test_png():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #register user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #upload photo
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
        'token': user_token['token'],
        'img_url': 'http://www.cse.unsw.edu.au/~richardb/index_files/RichardBuckland-200.png',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100,
    })
    assert resp.status_code == 400

#input error if x,y start/end not in dimensions of image URL
def test_invalid_x_start():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #register user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #upload photo
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
        'token': user_token['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg',
        'x_start': -1000,
        'y_start': 0,
        'x_end': 100,
        'y_end': 100,
    })
    assert resp.status_code == 400

def test_invalid_x_end():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #register user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #upload photo
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
        'token': user_token['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': -1000,
        'y_end': 100,
    })
    assert resp.status_code == 400

def test_invalid_y_start():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #register user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #upload photo
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
        'token': user_token['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg',
        'x_start': 0,
        'y_start': -1000,
        'x_end': 100,
        'y_end': 100,
    })
    assert resp.status_code == 400

def test_invalid_y_end():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #register user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #upload photo
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
        'token': user_token['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg',
        'x_start': 0,
        'y_start': 0,
        'x_end': 100,
        'y_end': -1000,
    })
    assert resp.status_code == 400

#input error if x_end < x_start
def test_x_end_less_than_x_start():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #register user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #upload photo
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
        'token': user_token['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg',
        'x_start': 5,
        'y_start': 0,
        'x_end': 2,
        'y_end': 100,
    })
    assert resp.status_code == 400

#input error if y_end < y_start
def test_y_end_less_than_y_start():
    #Reset route
    requests.delete(config.url + 'clear/v1')
    #register user
    user = requests.post(config.url + 'auth/register/v2', json={'email': 'validemail@gmail.com', 'password': '123abc!@#', 'name_first': 'Sam', 'name_last': 'Smith'})
    user_token = user.json()
    #upload photo
    resp = requests.post(config.url + 'user/profile/uploadphoto/v1', json={
        'token': user_token['token'],
        'img_url': 'http://cgi.cse.unsw.edu.au/~jas/home/pics/jas.jpg',
        'x_start': 0,
        'y_start': 5,
        'x_end': 100,
        'y_end': 2,
    })
    assert resp.status_code == 400


