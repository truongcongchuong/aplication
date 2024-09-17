import os
from werkzeug.utils import secure_filename
import bcrypt
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import base64


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/myProject"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'keyWord' 
db = SQLAlchemy(app)
loginManger = LoginManager()
loginManger.init_app(app)
loginManger.login_view = "Login"


STATIC = "static"
PATH_IMG = "IMG"
PATH_IMG_POST = f"{ PATH_IMG }/POST"
PATH_IMG_AVATAR = f"{ PATH_IMG }/AVATAR"
PATH_IMG_AVATAR_USER = f"{ PATH_IMG_AVATAR }/USER"
PATH_IMG_AVATAR_USER_DEFAULT = f"{ PATH_IMG_AVATAR_USER }/defaulf.png"
PATH_IMG_AVATAR_GROUP = f"{ PATH_IMG_AVATAR }/AVATAR/GROUP"
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff','.webp','.svg'}
TEMPLATE_LOGIN = "login/"


def check_fileName(fileName, FOULDER_UPLOAD):
    name, ext = os.path.splitext(fileName)
    count = 1
    new_fileName = f"{ name }_{ count }{ ext }"
    check_fileName = os.path.exists(os.path.join(FOULDER_UPLOAD, new_fileName))

    while check_fileName:
        count += 1
        new_fileName = f"{ name }_{ count }{ ext }"

    return new_fileName

def SaveFile(file, UPLOAD_FOULDER):

    fileName = secure_filename(file.filename)
    filePath = os.path.join(UPLOAD_FOULDER, fileName)
    name, ext = os.path.splitext(fileName)
    Status = False

    if ext in ALLOWED_EXTENSIONS:
        if os.path.exists(filePath):
            fileName = check_fileName(fileName, UPLOAD_FOULDER)

        try:
            file.save(filePath)
            Status = True
        except Exception as e:
            pass

    return fileName , Status
    
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
    # So sánh mật khẩu người dùng nhập với mật khẩu đã mã hóa
    return bcrypt.checkpw(user_password_bytes, hashed_password_bytes)