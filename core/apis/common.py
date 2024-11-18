from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import jwt,os,requests, base64
from core.libs.assertions import assert_valid, base_error

from werkzeug.datastructures import FileStorage

def gen_password(password):
    return generate_password_hash(password,method='pbkdf2:sha256')

def user_authentication_token(data,id):
    time = datetime.now()+timedelta(minutes=43200)
    exp = time.timestamp()
    payload = {"email":data['email'],"user_id":id, "expire":exp}
    temp = jwt.encode(payload, os.getenv('user_authorization_secret_key'), algorithm='HS256').decode('utf-8')
    return temp

def filestorage_to_base64(file_storage: FileStorage) -> str:
    file_content = file_storage.read()
    return base64.b64encode(file_content).decode('utf-8')

def save_image(data):
    url = 'https://api.imgur.com/3/upload'
    clientID = 'e0fd076cf8dcb5ff0524eb7714966200536e0a9c'
    headers = {'Authorization': 'Client-ID ' + '36f5b9e5d58c60a'}

    img = filestorage_to_base64(data)

    requestBody = {
        "image": img,
        "type":"base64",
        "title":"Test File",
        "description": "Test description"
    }

    response = requests.post(url, data=requestBody, headers=headers, verify=False)
    if response.status_code == 200:
        json_data = response.json()
        image_link = json_data['data']['link']
        return image_link
    else:
        print(response)
        return {"error": "ok"}