import bcrypt 
import base64

def hash_password(password):
    # Chuyển mật khẩu từ chuỗi thành byte
    password_bytes = password.encode('utf-8')
    
    # Sinh một "salt" để thêm vào trước khi mã hóa
    salt = bcrypt.gensalt()
    
    # Mã hóa mật khẩu
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
    
    return hashed_password_str

# Kiểm tra mật khẩu
def check_password(hashed_password, user_password):
    # Chuyển mật khẩu người dùng nhập vào thành byte
    user_password_bytes = user_password.encode('utf-8')
    # So sánh mật khẩu người dùng nhập với mật khẩu đã mã hóa
    return bcrypt.checkpw(user_password_bytes, hashed_password)

test = hash_password("chuong123")
print(test)
test2 = check_password(test, "chuong123")
print(test2)