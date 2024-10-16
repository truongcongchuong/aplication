import os
from werkzeug.utils import secure_filename
import bcrypt
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import base64


app = Flask(__name__)

UPLOAD_FOLDER = 'UPLOAD/'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/myProject_2"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'keyWord' 
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
db = SQLAlchemy(app)
loginManger = LoginManager()
loginManger.init_app(app)
loginManger.login_view = "Login"

# path mới
NUMBER_FILE_ALLOW_DISPLAY = 5
ALLOWED_EXTENSIONS_IMAGE = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff','.webp','.svg'}
ALLOWED_EXTENSIONS_VIDEO = {'.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm', '.3gp'}
STATIC_FOLDER = app.static_folder
UPLOAD_CONFIG_APP = app.config["UPLOAD_FOLDER"]
FOLDER_STATIC = ["UPLOAD"]
TEMPLATE = ["login", "page"]
UPLOAD = ["AVATAR", "POST"]
POST = ["POST", "REELS", "STORY"]


TEMPLATE__LOGIN = {
    "LOGIN": f"{TEMPLATE[0]}/Login.html",
    "FORGOT_PASSWORD" : f"{TEMPLATE[0]}/ForgotPassword.html",
    "REGISTER" : f"{TEMPLATE[0]}/Register.html"
}
TEMPLATE__PAGE = {
    "HOME": f"{TEMPLATE[1]}/Home.html",
    "MESSENGER": f"{TEMPLATE[1]}/Messenger.html",
    "PERSIONALL_INFOMATION": f"{TEMPLATE[1]}/PersionalInfomation.html",
    "REELS": f"{TEMPLATE[1]}/reels.html",
    "MOBAL_CREATE_POST": f"{TEMPLATE[1]}/CreatePost.html"
}
AVATAR = f"{FOLDER_STATIC[0]}/{UPLOAD[0]}/"
AVATAR_DEFAULF = f"{AVATAR}defaulf.png"

def PathUpload(userID):
    upload_file = {
        "POST": f"{UPLOAD[1]}/{userID}/{POST[0]}",
        "REELS": f"{UPLOAD[1]}/{userID}/{POST[1]}",
        "STORY": f"{UPLOAD[1]}/{userID}/{POST[2]}"
    }
    return upload_file

def check_fileName(fileName, FOULDER_UPLOAD):
    name, ext = os.path.splitext(fileName)
    count = 1
    new_fileName = f"{ name }_{ count }{ ext }"

    while os.path.exists(os.path.join(FOULDER_UPLOAD, new_fileName)) == True:
        count += 1
        new_fileName = f"{ name }_{ count }{ ext }"
        print(count)
        print("check file name", check_fileName)
        print("new file", new_fileName)

    return new_fileName

def SaveFile(file, UPLOAD_FOULDER):

    fileName = secure_filename(file.filename)
    name, ext = os.path.splitext(fileName)

    if ext in ALLOWED_EXTENSIONS_IMAGE or ext in ALLOWED_EXTENSIONS_VIDEO:
        if os.path.exists(os.path.join(UPLOAD_FOULDER, fileName)):
            fileName = check_fileName(fileName, UPLOAD_FOULDER)
            print(fileName)
        try:
            file.save(os.path.join(UPLOAD_FOULDER, fileName))
            print("upload file thành công")
            return fileName
        except Exception as e:
            print(f"upload file thất bại: {e}")
            return None
    else:
        return None

    
# Mã hóa mật khẩu
def hash_password(password):
    password_bytes = password.encode('utf-8')
    
    salt = bcrypt.gensalt()
    
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
    
    return hashed_password_str

def check_password(hashed_password, user_password):
    user_password_bytes = user_password.encode('utf-8')
    hashed_password_bytes = base64.b64decode(hashed_password)
    return bcrypt.checkpw(user_password_bytes, hashed_password_bytes)