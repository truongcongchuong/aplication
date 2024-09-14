import os
from werkzeug.utils import secure_filename
import bcrypt
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'keyWord' 
db = SQLAlchemy(app)
loginManger = LoginManager()
loginManger.init_app(app)
loginManger.login_view = "Login"


STATIC = "static"
PATH_IMG =f"{ STATIC }/IMG"
PATH_IMG_POST = f"{ PATH_IMG }/POST"
PATH_IMG_AVATAR = f"{ PATH_IMG }/AVATAR"
PATH_IMG_AVATAR_USER = f"{ PATH_IMG_AVATAR }/AVATAR/USER"
PATH_IMG_AVATAR_GROUP = f"{ PATH_IMG_AVATAR }/AVATAR/GROUP"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
TEMPLATE_LOGIN = "login/"

def find_unique_filenName(fileName, UPLOAD_FOUDER):
    name, ext = os.path.splitext(fileName)
    counter = 1
    new_fileName = f"{ name }_{ counter }{ ext }"
    check_fileName = os.path.exists(os.path.join(UPLOAD_FOUDER, new_fileName))

    while check_fileName:
        counter += 1
        new_fileName = f"{ name }_{ counter }{ ext }"
    
    return new_fileName

def SaveFile(file, UPLOAD_FOUDER):

    fileName = secure_filename(file.filename)
    filePath = os.path.join(UPLOAD_FOUDER, fileName)
    name, ext = os.path.splitext(fileName)
    Status = False

    if ext in ALLOWED_EXTENSIONS:
        if os.path.exists(filePath):
            fileName = find_unique_filenName(fileName, UPLOAD_FOUDER)

        try:
            file.save(os.path.join(UPLOAD_FOUDER, fileName))
            Status = True
        except:
            exit()

    return fileName , Status
    
# Mã hóa mật khẩu
def hash_password(password):
    # Chuyển mật khẩu từ chuỗi thành byte
    password_bytes = password.encode('utf-8')
    
    # Sinh một "salt" để thêm vào trước khi mã hóa
    salt = bcrypt.gensalt()
    
    # Mã hóa mật khẩu
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_password

# Kiểm tra mật khẩu
def check_password(hashed_password, user_password):
    # Chuyển mật khẩu người dùng nhập vào thành byte
    user_password_bytes = user_password.encode('utf-8')
    
    # So sánh mật khẩu người dùng nhập với mật khẩu đã mã hóa
    return bcrypt.checkpw(user_password_bytes, hashed_password)