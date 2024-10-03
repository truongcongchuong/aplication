from datetime import datetime
from flask_login import UserMixin
from module import db


class Gender(db.Model):
    __tablename__ = "Gender"
    id = db.Column(db.Integer, primary_key = True)
    GenderName = db.Column(db.String(50), unique=True)
class Users(UserMixin,db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key = True)
    UserName = db.Column(db.String(50), nullable = False)
    Account = db.Column(db.String(50), unique = True)
    Password = db.Column(db.String(200), nullable = False)
    Gmail = db.Column(db.String(100), unique = True)
    PhoneNumber = db.Column(db.String(50), unique = True)
    Gender = db.Column(db.Integer, db.ForeignKey("Gender.id"))
    Birthday = db.Column(db.DateTime)
    Avatar = db.Column(db.String(200), unique = True)

class Friend(db.Model):
    __tablename__ = "Friend"
    UserID = db.Column(db.Integer,db.ForeignKey("Users.id"), primary_key = True)
    Friend = db.Column(db.Integer,db.ForeignKey("Users.id"), primary_key = True)

# bảng nhóm chat
# nhóm chat được chi thành 2 loại là nhóm chát cá nhân tức là 2 người ib cho nhau
# loại thứ 2 sẽ là một nhóm người nhắn tin với nhau
class TypeGroupChat(db.Model):
    __tablename__ = "TypeGroupChat"
    id = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(50), unique=True)
class GroupChat(db.Model):
    __tablename__ = "GroupChat"
    id = db.Column(db.Integer, primary_key = True)
    GroupName = db.Column(db.String(50), nullable = False)
    Admin = db.Column(db.Integer, db.ForeignKey("Users.id"))
    TypeGroup = db.Column(db.Integer, db.ForeignKey("TypeGroupChat.id"))
    Avatar = db.Column(db.String(200), unique = True)

class MemberGroup(db.Model):
    __tablename__ = "MemberGroup"
    GroupID = db.Column(db.Integer, db.ForeignKey("GroupChat.id"), primary_key = True)
    Member = db.Column(db.Integer, db.ForeignKey("Users.id"), primary_key = True)
    date_join = db.Column(db.DateTime, default= datetime.now)
# bang lu tru cac doan chat messenger
class Messenger(db.Model):
    __tablename__ = "Messenger"
    id = db.Column(db.Integer, primary_key = True)
    Sender = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = True) 
    Addressee = db.Column(db.Integer, db.ForeignKey("GroupChat.id"), nullable = True)
    Messenger = db.Column(db.Text)
    sendingTime = db.Column(db.DateTime, default= datetime.now)
class MessengerFile(db.Model):
    __tablename__ = "MessengerFile"
    id = db.Column(db.Integer, primary_key = True)
    path = db.Column(db.Text, unique = True)
    messenger = db.Column(db.Integer,  db.ForeignKey("Messenger.id"), nullable = True) 
# luu tru cac bai dang cua nguoi dung
class SavePost(db.Model):
    __tablename__ = "SavePost"
    UserSave = db.Column(db.Integer, db.ForeignKey("Users.id"), primary_key = True)
    post = db.Column(db.Integer,  db.ForeignKey("Post.id"), primary_key = True)
    date_save = db.Column(db.DateTime,  default= datetime.now)

class TypePost(db.Model):
    __tablename__ = "TypePost"
    id = db.Column(db.Integer, primary_key = True) 
    TypeName = db.Column(db.String(100), unique = True)
    Number_of_file_upload = db.Column(db.Integer)
class Post(db.Model):
    __tablename__ = "Post"
    id = db.Column(db.Integer, primary_key = True)
    UserPost = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = True)
    caption = db.Column(db.Text)
    TypePost = db.Column(db.Integer, db.ForeignKey("TypePost.id"), nullable = True)
    posting_date = db.Column(db.DateTime,  default= datetime.now)
# comment
class Comment(db.Model):
    __tablename__ = "Comment"
    id = db.Column(db.Integer, primary_key = True)
    UserComment = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = True)
    Post = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable = True)
    comment = db.Column(db.Text, nullable = True)
    CommentTime = db.Column(db.DateTime,  default= datetime.now)

# thong tin ve cac bieu cam
class Emotion(db.Model):
    __tablename__ = "Emotion"
    id = db.Column(db.Integer, primary_key = True)
    ImotionName = db.Column(db.String(100), unique = True)
    Emoji = db.Column(db.String(100))

class Feeling(db.Model):
    __tablename__ = "Feeling"
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), primary_key = True)
    post = db.Column(db.Integer, db.ForeignKey("Post.id"), primary_key = True)
    emoji = db.Column(db.Integer, db.ForeignKey("Emotion.id"), nullable = True)