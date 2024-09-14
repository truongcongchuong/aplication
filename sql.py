from datetime import datetime
from flask_login import UserMixin
from module import db


class Users(UserMixin,db.Model):
    __tablename__ = "Users"
    UserID = db.Column(db.Integer, primary_key = True)
    UserName = db.Column(db.String(50), nullable = False)
    Account = db.Column(db.String(50), unique = True)
    Password = db.Column(db.String(200), nullable = False)
    Gmail = db.Column(db.String(100), unique = True)
    PhoneNumber = db.Column(db.String(50), unique = True)
    Avatar = db.Column(db.String(200), unique = True)

class Friend(db.Model):
    __tablename__ = "Friend"
    UserID = db.Column(db.Integer,db.ForeignKey("Users.UserID"), primary_key = True)
    Friend = db.Column(db.Integer,db.ForeignKey("Users.UserID"), primary_key = True)

class Group(db.Model):
    __tablename__ = "Group"
    GroupID = db.Column(db.Integer, primary_key = True)
    GroupName = db.Column(db.String(50), nullable = False)
    Admin = db.Column(db.Integer, db.ForeignKey("Users.UserID"))
    Avatar = db.Column(db.String(200), unique = True)

class MemberGroup(db.Model):
    __tablename__ = "MemberGroup"
    GroupID = db.Column(db.Integer, db.ForeignKey("Group.GroupID"), primary_key = True)
    Member = db.Column(db.Integer, db.ForeignKey("Users.UserID"), primary_key = True)

# lưu trữ các đoạn tin nhắn của các nhóm
class ChatGroup(db.Model):
    __tablename__ = "ChatGroup"
    Sender = db.Column(db.Integer, db.ForeignKey("Users.UserID"), primary_key = True)
    GroupID = db.Column(db.Integer, db.ForeignKey('Group.GroupID'), primary_key = True)
    Messenger = db.Column(db.String(200), nullable = False)
    SendingTime = db.Column(db.DateTime,default= datetime.now, primary_key = True)

# lưu trữ các đoạn tin nhắn các nhân giữa các người dùng với nhau 
class Messenger(db.Model):
    __tablename__ = "Messenger"
    Sender = db.Column(db.Integer, db.ForeignKey("Users.UserID"), primary_key = True)
    Addressee = db.Column(db.Integer, db.ForeignKey('Users.UserID'), primary_key = True)
    Messenger = db.Column(db.String(500), nullable = False)
    SendingTime = db.Column(db.DateTime,default= datetime.now, primary_key = True)

class Post(db.Model):
    __tablename__ = "Post"
    PostID = db.Column(db.Integer, primary_key = True)
    UsetPost = db.Column(db.Integer, db.ForeignKey('Users.UserID'))
    Caption = db.Column(db.String(200), nullable = False)
    PortTime = db.Column(db.DateTime, default= datetime.now)

class PostImg(db.Model):
    __tablename__ = "PostImg"
    pathIng = db.Column(db.String(200), )
    PostID = db.Column(db.Integer, primary_key = True, nullable = False)

class Comment(db.Model):
    __tablename__ = "Comment"
    PostID = db.Column(db.Integer,db.ForeignKey("Post.PostID") ,primary_key = True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID'), primary_key = True)
    Comment = db.Column(db.String(200), nullable = False)
    PortTime = db.Column(db.DateTime, primary_key = True, default= datetime.now)