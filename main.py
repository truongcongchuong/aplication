
from module import *
from sql import *
from flask import  request,render_template,redirect, url_for, flash
from flask_login import logout_user, login_required, current_user, login_user
from sqlalchemy.exc import IntegrityError

def main():
    with app.app_context():
        db.create_all()

@loginManger.user_loader
def load_user(id):
    user = Users.query.get(int(id))
    path = f"{UPLOAD_CONFIG_APP}{UPLOAD[1]}/{id}"
    if os.path.exists(path) == False:
        os.makedirs(path, exist_ok=True)
        for subdirectory in POST:
            subdirectory_path = os.path.join(path, subdirectory)
            os.mkdir(subdirectory_path)

    return user
# trang chủ  
@app.route("/")
@login_required
def Home():
    
    return render_template(TEMPLATE__PAGE["HOME"],
                           user = current_user,
                           avatar = AVATAR)

# đăng nhập và đăng ký tài khoản
@app.route("/Login", methods = ['GET', 'POST'])
def Login():
    if request.method == "POST":
        Account = request.form["Account"]
        Password = request.form["Password"]
        AccountUser = Users.query.filter_by(Account = Account).first()
        if AccountUser:
            check = check_password(AccountUser.Password, Password )
            if check:
                login_user(AccountUser)
                return redirect(url_for('Home'))
            else:
                flash("Your password is incorrect", "error")
        else:
            flash("account does not exist","error")
    return render_template(TEMPLATE__LOGIN["LOGIN"])

@app.route("/Register", methods = ["GET", "POST"])
def Register():
    option = Gender.query.all()  
    if request.method == "POST":
        UserName = request.form["UserName"]
        Account = request.form["Account"]
        Password = request.form["Password"]
        confirmPassword = request.form["confirmPassword"]
        Gmail = request.form["Gmail"]
        PhoneNumber = request.form["PhoneNumber"]
        Avatar = request.files["Avatar"]
        BirthDay = request.form["Birthday"]
        gender = request.form["gender"]
        duplicateError = "Duplicate entry"
        duplicateAccount = f"{ duplicateError } '{ Account }' for key 'Account'"
        duplicateGmail = f"{ duplicateError } '{ Gmail }' for key 'Gmail'"
        duplicatePhoneNumber = f"{ duplicateError } '{ PhoneNumber }' for key 'PhoneNumber'"
                
        if Password == confirmPassword:
            PasswordHash = hash_password(Password)
            user = Users(
                UserName = UserName,
                Account = Account,
                Password =  PasswordHash,
                Gmail = Gmail,
                PhoneNumber = PhoneNumber,
                Gender = gender,
                Birthday = BirthDay
            )
            try:
                db.session.add(user)
                db.session.commit()

                fileName = "defaulf.png"
                if Avatar.filename != '':
                    Name, Status = SaveFile(Avatar,AVATAR)
                    if Status == True:
                        fileName = Name  

                Users.query.filter_by(Account = Account).update(dict(Avatar = fileName))
                db.session.commit()
                flash("register successfully", "success")
                return redirect(url_for("Login"))
            except IntegrityError as e:
                db.session.rollback() # hoàn tác lại thay đổi nếu có lỗi
                if duplicateAccount in str(e):
                    flash("account already exists", "error")
                    Account = ""
                if duplicateGmail in str(e):
                    flash("Gmail already exists", "error")
                    Gmail = ""
                if duplicatePhoneNumber in str(e):
                    flash("Phone number already exists", "error")
                    PhoneNumber = ""
        else: 
            flash("Confirmation password is incorrect", "error")
            Password = ""
            confirmPassword = ""
        return render_template(TEMPLATE__LOGIN["REGISTER"],
                                fileAccept = ALLOWED_EXTENSIONS,
                                account = Account,
                                gmail = Gmail,
                                phoneNumber = PhoneNumber,
                                userName = UserName, 
                                password = Password,
                                confirmPassword = confirmPassword,
                                avatarDefault = PATH_IMG_AVATAR_USER_DEFAULT,
                                gender = option)  

    return render_template(TEMPLATE__LOGIN["REGISTER"],
                            fileAccept = ALLOWED_EXTENSIONS,
                            avatarDefault = PATH_IMG_AVATAR_USER_DEFAULT,
                            gender = option)    

@app.route("/ForgotPasword", methods = ["GET", "POST"])
def take_back_password():
    
    if request.method == "POST":
        Account = request.form["Account"]
        Gmail = request.form["Gmail"]
        PhoneNumber = request.form["PhoneNumber"]
        NewPassword = request.form["NewPassword"]
        confirmPassword = request.form["confirmPassword"]
        flash(f"{NewPassword} mật khẩu mới")
        flash(f"{ confirmPassword } xác nhận mật khẩu")
        if confirmPassword == NewPassword:
            user = db.session.query(
            Users.Gmail, Users.PhoneNumber
            ).filter(
                Users.Account == Account
                ).first()
            if user:
                if user.Gmail == Gmail and user.PhoneNumber == PhoneNumber:
                    try:
                        Password = hash_password(NewPassword)
                        Users.query.filter(Users.Account == Account).update({Users.Password: Password})
                        db.session.commit()
                        flash("Changes password successfully", "success")
                        return redirect(url_for("Login"))
                    except:
                        pass
                if user.Gmail != Gmail:
                    flash("gmail is incorrect", "error")
                if user.PhoneNumber != PhoneNumber:
                    flash("gmail is incorrect", "error")
            else:
                flash("account not found", "error")
        else:
            flash("Confirmation password is incorrect", "error")

    return render_template(TEMPLATE__LOGIN["FORGOT_PASSWORD"])
# thông tin cá nhân
@app.route("/Persional_information")
@login_required
def Persional_information():
    return render_template(TEMPLATE__PAGE["PERSIONALL_INFOMATION"], user = current_user)
# tạo bài viết
@app.route("/CreatePost", methods=["POST", "GET"])
def CreatePost():
    if request.method == "POST":
        pass
    #return render_template(TEMPLATE__PAGE["MOBAL_CREATE_POST"])
    return render_template(TEMPLATE__PAGE["MOBAL_CREATE_POST"])
@app.route("/Messenger")
@login_required
def messenger(): 
    return render_template(TEMPLATE__PAGE["MESSENGER"], user = current_user)
@app.route("/Reals")
def Reals():
    return render_template(TEMPLATE__PAGE["REELS"])
@app.route("/LogOut")
@login_required
def LogOut():
    logout_user()
    return redirect(url_for("Login"))

if __name__ == "__main__":
    main()
    app.run(debug=True)