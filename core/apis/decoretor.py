from functools import wraps
from flask import request
import os,jwt
from core.libs.assertions import assert_found, assert_valid, base_error
from datetime import datetime

def accept_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        incoming_payload = request.json
        return func(incoming_payload, *args, **kwargs)
    return wrapper

def accept_car_payload(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        title = request.form.get('title')
        description = request.form.get('description')
        tags = request.form.get('tags')
        
        images = request.files.getlist('images')
        uploaded_files = []
        for image in images:
            if image.filename:
                uploaded_files.append(image)
        
        payload = {
            "title": title,
            "description": description,
            "tags": tags,
            "images": uploaded_files
        }
        
        return func(self, payload, *args, **kwargs)
    return wrapper

def verify_token(token, secret_key):
    try:
        data=jwt.decode(token, secret_key, algorithms=['HS256'])
        return data['user_id']
    except:
        base_error(406,{"message":"invalid token"})
        assert_valid(data['expire']>int(datetime.now().timestamp()),"login expired !!!")

def user_authorization_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token=request.headers.get(os.getenv('user_authorization_header_key'))
        assert_found(token, "Authorization token is missing")
        user_id = verify_token(token, os.getenv('user_authorization_secret_key'))
        return func(user_id, *args, **kwargs)
    return wrapper
