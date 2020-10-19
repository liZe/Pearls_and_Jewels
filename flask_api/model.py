from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column,String, Integer, ForeignKey, DateTime
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///model.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Tables of project


class User(db.Model):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    login = Column(String(25), unique=True, nullable=False)
    password = Column(String(50), nullable=False)


class Pearls(db.Model):
    __tablename__ = "PearlsAndJewels"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    content = Column(String(300), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


class Comments(db.Model):
    __tablename__ = "Comments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.id'))
    pearl_id = Column(Integer, ForeignKey('Pearls.id'))
    comment = Column(String(200), nullable=False)


class Smileys(db.Model):
    __tablename__ = "Smileys"
    id = Column(Integer, primary_key=True)
    alt_name = Column(String(25), nullable=False)
    img_link = Column(String, nullable=False)


class Associations(db.Model):
    __tablename__ = "Associations"
    user_id = Column(Integer, ForeignKey('User.id'), primary_key=True)
    smiley_id = Column(Integer, ForeignKey('Smileys.id'), primary_key=True)
    pearl_id = Column(Integer, ForeignKey('Pearls.id'), primary_key=True)