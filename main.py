
from module import *
from sql import *
from flask import  request,render_template,redirect, url_for, flash
from flask_login import logout_user, login_required, current_user, login_user
from sqlalchemy.exc import IntegrityError
import mimetypes
from sqlalchemy import or_


def main():
    with app.app_context():
        db.create_all()

@loginManger.user_loader
def load_user(id):
    user = db.session.get(Users, int(id))
    path = f"{UPLOAD_CONFIG_APP}{UPLOAD[1]}/{id}"
    if os.path.exists(path) == False:
        os.makedirs(path, exist_ok=True)
        for subdirectory in POST:
            subdirectory_path = os.path.join(path, subdirectory)
            os.mkdir(subdirectory_path)

    return user
# trang chủ  
@app.route("/", methods = ['GET', 'POST'])
@login_required
def Home():
    
    if request.method == "POST":
        pass
    # xử lý hiển thị các bài đăng
    posts = (
        db.session.query(
            Post.id,
            Post.caption, 
            Post.posting_date, 
            Post.UserPost,
            Users.UserName,
            Users.Avatar,
            TypePost.TypeName 
            )
        .join(Post, Post.UserPost == Users.id)
        .join(TypePost, TypePost.id == Post.TypePost)
        .filter(or_(TypePost.TypeName == "POST",TypePost.TypeName == "STORY"))
        .order_by(Post.posting_date.desc())
        .all()
    )
    html_post = ""
    html_story = ""
    for post in posts:
        if post:
            file_post = (
                db.session.query(FilePost.fileName)
                .join(Post, Post.id == FilePost.post)
                .filter(FilePost.post == post.id )
                .all()
            )
            path_file_upload = PathUpload(post.UserPost)
            # hiển thị các bài đăng POST
            if post.TypeName == "POST":
                display_file = ""
                count = 0
                for file in file_post:
                    if file:
                        name, ext = os.path.splitext(file.fileName)

                        if count <= NUMBER_FILE_ALLOW_DISPLAY:
                            if ext in ALLOWED_EXTENSIONS_IMAGE:
                                count += 1
                                display_file += f"""
                                    <img id="file_{count}" src='{url_for("static", filename=f"{UPLOAD_CONFIG_APP}{path_file_upload["POST"]}/{file.fileName}")}'>
                                """
                            elif ext in ALLOWED_EXTENSIONS_VIDEO:
                                count += 1
                                mime_type, encoding = mimetypes.guess_type(file.fileName)

                                display_file += f"""
                                                    <video id="file_{count}" controls style="max-height: 400px;" width="100%" height="100%">
                                                        <source type="{mime_type}" src="{url_for("static", filename=f"{UPLOAD_CONFIG_APP}{path_file_upload["POST"]}/{file.fileName}")}">
                                                    </video>
                                                """
                        else:
                            count += 1
                            

                # hiển thị tất cả thông tin của bài đăng
                name_class = f"preview-{ count }-file"

                if count > NUMBER_FILE_ALLOW_DISPLAY:

                    name_class = "display-out-file"
                    display_file += f"""
                                        <div id="out-of-range">
                                            + {count - NUMBER_FILE_ALLOW_DISPLAY}
                                        </div>
                                    """

                html_post += f"""
                    <li>
                        <div class="post">
                            <div id="information-user-post">
                                <img src="{ url_for("static", filename=f"{AVATAR}{post.Avatar}")}" alt="">
                                <span>{post.UserName}</span>
                                <button><i class="bi bi-three-dots"></i><button>
                            </div>
                            <div class="caption">
                                <p>{post.caption}</p>
                            </div>
                            <div class="media-post">
                                <button class="{name_class}" type="button">
                                    {display_file}
                                </button>
                            </div>
                        </div>
                        <div class="interact">
                            <button><i class="bi bi-suit-heart"></i><span>Like</span></button>
                            <button><i class="bi bi-chat"></i><span>Comment</span></button>
                            <button><i class="bi bi-bookmarks-fill"></i><span>Save</span></button>
                        </div>
                    </li>
                """
            # hiển thị các bài đăng STORY
            elif post.TypeName == "STORY":
                mime_type, encoding = mimetypes.guess_type(file.fileName)
                html_story += f"""
                                    <li>
                                        <button>
                                            <img id="user-post" src="{url_for("static", filename=f"{AVATAR}{post.Avatar}")}">
                                            <video id="story"  width="100%" height="100%"  disabled>
                                                <source src="{url_for("static", f"{UPLOAD_CONFIG_APP}{path_file_upload["STORY"]}/{file.fileName}")}" type="{mime_type}">
                                            </video>
                                            <p id="username_post">{ post.UserName }</p>
                                        </button>
                                    </li>
                                """
        else:
            pass
    if html_post == "":
        html_post += """"
                        <li class="none-post">
                            <div id="icon-text">
                                <i class="bi bi-check2-circle"></i>
                            </div>
                            <h1>You have seen all the posts</h1>
                        </li>
                    """
    if html_story =="":
        pass
    return render_template(TEMPLATE__PAGE["HOME"],
                           user = current_user,
                           avatar = AVATAR,
                           html_post = html_post
                           )

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
                    fileName = SaveFile(Avatar,f"{STATIC_FOLDER}{STATIC_FOLDER}{AVATAR}") 

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
                                fileAccept = ALLOWED_EXTENSIONS_IMAGE,
                                account = Account,
                                gmail = Gmail,
                                phoneNumber = PhoneNumber,
                                userName = UserName, 
                                password = Password,
                                confirmPassword = confirmPassword,
                                avatarDefault = AVATAR_DEFAULF,
                                gender = option)  

    return render_template(TEMPLATE__LOGIN["REGISTER"],
                            fileAccept = ALLOWED_EXTENSIONS_IMAGE,
                            avatarDefault = AVATAR_DEFAULF,
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
            user = (db.session.query(
                Users.Gmail, 
                Users.PhoneNumber
            )
            .filter(Users.Account == Account)
            .first())
            if user:
                if user.Gmail == Gmail and user.PhoneNumber == PhoneNumber:
                    try:
                        Password = hash_password(NewPassword)
                        Users.query.filter(Users.Account == Account).update({Users.Password: Password})
                        db.session.commit()
                        flash("Changes password successfully", "success")
                        return redirect(url_for("Login"))
                    except:
                        db.session.rollback()
                        flash("change password failed ", "error")
                    finally:
                        db.session.close()
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
        caption = request.form["caption"]
        filePost = request.files.getlist("files[]")
        typePost = request.form["typePost"]
        
        information_type_post = (db.session.query(
                TypePost.Number_of_file_upload,
                TypePost.TypeName
            )
            .filter(TypePost.id == typePost)
            .first())

        if len(filePost) <= int(information_type_post.Number_of_file_upload):
            try:
                post = Post(
                        UserPost = current_user.id,
                        caption = caption,
                        TypePost = typePost
                    )
                db.session.add(post)
                db.session.commit()

                print(filePost)
                for file in filePost:
                    if file:
                        path = PathUpload(current_user.id)
                        filename = SaveFile(file, f"{STATIC_FOLDER}{UPLOAD_CONFIG_APP}{path[information_type_post.TypeName]}")
                        print(filename)
                        if filename != None:
                            PostId = (db.session.query(
                                    Post.id
                                )
                                .filter( Post.UserPost == current_user.id)
                                .order_by(Post.id.desc())
                                .first()
                            )
        
                            add_db_file_post = FilePost(
                                fileName = filename,
                                post = PostId.id
                            )
                            db.session.add(add_db_file_post)
                            db.session.commit()
                        else:
                            db.session.rollback()
                            flash("Posting failed", "error")
                    else:
                        flash("The uploaded file is corrupted", "error")
                flash("Posting successfully", "success")
        
            except ZeroDivisionError as e:
                db.session.rollback()
                print(e)
                flash("Posting Failed", "error")
            finally:
                db.session.close()
                return redirect(url_for("Home"))
        else:
            flash(f"{typePost} only can post {information_type_post.Number_of_file_upload} file", "error")

    kind_of_post = TypePost.query.all()
    return render_template(TEMPLATE__PAGE["MOBAL_CREATE_POST"], typePost = kind_of_post)

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