
from module import *
from sql import *
from flask import  request,render_template,redirect, url_for, flash
from flask_login import logout_user, login_required, current_user, login_user


def main():
    with app.app_context():
        db.create_all()

@loginManger.user_loader
def load_user(UserID):
    return Users.query.get(UserID)
    
@app.route("/")
@login_required
def Home():
    return render_template("index.html", user = current_user)

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
                pass
    return render_template(f"{ TEMPLATE_LOGIN }login.html")

@app.route("/Register", methods = ["GET", "POST"])
def Register():
    if request.method == "POST":
        UsersName = request.form["UserName"]
        Account = request.form["Account"]
        Password = request.form["Password"]
        confirmPassword = request.form["confirmPassword"]
        Gmail = request.form["Gmail"]
        PhoneNumber = request.form["PhoneNumber"]
        Avatar = request.files["Avatar"]
        
        if Password == confirmPassword:
            Password = hash_password(Password)
            fileName, Status = SaveFile(Avatar, PATH_IMG_AVATAR_USER)
            if Status == True:
                user = Users(
                    UsersName = UsersName,
                    Account = Account,
                    Password = Password,
                    Gmail = Gmail,
                    PhoneNumber = PhoneNumber,
                    Avatar = fileName
                )
                db.session.add(user)
                db.commit()
                return redirect(url_for("Login"))
        else:
            pass
    return render_template(f"{ TEMPLATE_LOGIN }register.html", fileAccept = ALLOWED_EXTENSIONS)

@app.route("/ForgotPasword", methods = ["GET", "POST"])
def take_back_password():
    
    if request.method == "POST":
        Account = request.form["Account"]
        Gmail = request.form["Gmail"]
        PhoneNumber = request.form["PhoneNumber"]
        NewPassword = request.form["NewPassword"]
        confirmPassword = request.form["confirmPassword"]

        user = db.session.query(
            Users.Gmail, Users.PhoneNumber
            ).filter(
                Users.Account == Account
                ).first()
        if user:
            if confirmPassword == NewPassword:
                if user.Gmail == Gmail and user.PhoneNumber == PhoneNumber:
                    Password = hash_password(NewPassword)
                    Users.query.filter(Users.Account == Account).update({Users.Password: Password})
                    db.session.commit()
                    return redirect(url_for("Login"))
                else:
                    pass
        else:
            pass

    return render_template(f"{ TEMPLATE_LOGIN }ForgotPassword.html")

@app.route("/Persional_information")
@login_required
def Persional_information():
    return render_template("PersionalInfomation.html", user = current_user)
@app.route("/LogOut")
@login_required
def LogOut():
    logout_user()
    return redirect(url_for("Login"))
    
if __name__ == "__main__":
    main()
    app.run(debug=True)