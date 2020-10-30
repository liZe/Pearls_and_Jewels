from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, String, Integer, ForeignKey, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps
import sqlite3
from pprint import pprint

# Database name
database_name = "model.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + database_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SECRET_KEY'] = 'configurestrongsecretkeyhere'

db = SQLAlchemy(app)


"""
*** CONNECTION to the Database file
"""

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


"""
*** CLASSES Database model
"""

class User(db.Model):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)

    # Connection to the database
    conn = create_connection(database_name)

    # Method to give a role (User lambda by default)
    def role_user(self):
        role = "Basic User"  # By default, an user is a basic user

    # Method extract privileges for specific user
    def get_privilege_user(self):
        tab_privileges = []
        cur = self.conn.cursor()

        cur.execute("""SELECT type, grants.name_grant, grants.id
                            FROM USERS
                                inner join Association_User on USERS.id=Association_User.user_id
                                inner join GRANTS on GRANTS.id=Association_User.granted_id
                            WHERE users.id=""" + str(self.id))
        rows = cur.fetchall()
        for row in rows:
            if row[0] == "Role":
                self.list_roles_and_rights(row[2], tab_privileges)
            else:
                tab_privileges.append(row[1])
        return tab_privileges

    # Method list privileges and roles associated for specific user
    def list_roles_and_rights(self, id_role, privileges):
        cur = self.conn.cursor()
        cur.execute("""SELECT grants_grantee.name_grant, grants_granted.name_grant, grants_granted.id, grants_granted.type
                    FROM Association_Grant
                        inner join GRANTS as grants_grantee on grants_grantee.id = Association_Grant.grantee_id
                        inner join GRANTS as grants_granted on grants_granted.id = Association_Grant.granted_id
                    WHERE grantee_id=""" + str(id_role))
        rows = cur.fetchall()
        for row in rows:
            if row[3] == "Role":
                self.list_roles_and_rights(row[2], privileges)
            else:
                privileges.append(row[1])



class Pearl(db.Model):
    __tablename__ = "PearlsAndJewels"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    content = Column(String(300), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


class Comment(db.Model):
    __tablename__ = "Comments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    pearl_id = Column(Integer, ForeignKey('PearlsAndJewels.id'))
    comment = Column(String(200), nullable=False)


class Smiley(db.Model):
    __tablename__ = "Smileys"
    id = Column(Integer, primary_key=True)
    alt_name = Column(String(25), nullable=False)
    img_link = Column(String, nullable=False)


class Associations(db.Model):
    __tablename__ = "Associations"
    user_id = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    smiley_id = Column(Integer, ForeignKey('Smileys.id'), primary_key=True)
    pearl_id = Column(Integer, ForeignKey('PearlsAndJewels.id'), primary_key=True)


class Grant(db.Model):
    __tablename__ = "Grants"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    name_grant = Column(String, nullable=False)
    comment_grant = Column(String)


class AssoGrant(db.Model):
    __tablename__ = "Association_Grant"
    grantee_id = Column(String, ForeignKey(Grant.id), primary_key=True)
    granted_id = Column(String, ForeignKey(Grant.id), primary_key=True)


class AssoUser(db.Model):
    __tablename__ = "Association_User"
    user_id = Column(String, ForeignKey(User.id), primary_key=True)
    granted_id = Column(String, ForeignKey(Grant.id), primary_key=True)



def get_user_from_token(token, secret_key):
    try:
        username = jwt.decode(token, secret_key)
        user = db.session.query(User).filter(User.username == username['user']).first()
        return user
    except:
        return None




@app.route("/check_token", methods=["POST"])
def check_login(*args, **kwargs):
    logs = request.get_json()
    if 'token' in logs:
        try:
            jwt.decode(logs['token'], app.config['SECRET_KEY'])
        except:
            return jsonify({"error": "token is invalid"}), 401
    return jsonify({"message": "token is valid"}), 200


"""
wrapper used to protect route that need the user to be logged in
"""
def login_required(f):
    @wraps(f)
    def check_login(*args, **kwargs):
        logs = request.get_json()
        if 'token' in logs:
            try:
                jwt.decode(logs['token'], app.config['SECRET_KEY'])
            except:
                return jsonify({"error": "token is invalid"}), 401
        return f(*args, **kwargs)
    return check_login

@app.route("/register", methods=["POST"])
def register():
    logs = request.get_json()
    if logs['password'] != logs['passwordBis']:
        return jsonify({'error': 'Les mots de passe ne correspondent pas.'}), 500
    try:
        db.session.add(User(username=logs['userName'], password=generate_password_hash(logs['password'])))
        db.session.commit()
        return jsonify({'message': 'Votre compte a ete cree'}), 200
    except:
        return jsonify({"error": "une erreur est intervenue"}), 500

@app.route("/login", methods=["POST"])
def login():
    logs = request.get_json()
    user = db.session.query(User).filter(User.username == logs['userName']).first()
    if user and check_password_hash(user.password, logs['password']):
        token = jwt.encode({'user': logs['userName'], 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        response = make_response({"message": "user logged in"})
        response.set_cookie('token', token.decode('UTF-8'))
        return response
    return jsonify({'error': 'username or password incorrect'}), 500


@app.route('/profile', methods=["POST"])
def profile():
    data = request.get_json()
    try:
        user = get_user_from_token(data['token'], app.config['SECRET_KEY'])
        return jsonify({'username': user.username,'password': user.password, 'date_creation': user.date_creation}), 200
    except Exception as e:
        return jsonify({'error': 'unexcpected error '}), 401


@app.route('/delete_account', methods=["POST"])
@login_required
def delete_account():
    data = request.get_json()
    user = get_user_from_token(data['token'], app.config['SECRET_KEY'])
    try:
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'account deleted !'}), 200
    except Exception as e:
        return jsonify({'error': 'unexpected error '}), 401


"""
*** Invironment config
*** If tables doesn't exists, create it
"""
# Doc sqlalchemy : "Conditional by default, will not attempt to recreate tables already present in the target database."
db.create_all()

"""
*** Load statics roles configuration if needed
"""


def insert_without_integrity_check(text_insert):
    conn = create_connection(database_name)
    cur = conn.cursor()
    try:
        cur.execute(text_insert)
        conn.commit()
    except sqlite3.IntegrityError as e:
        pass


def load_static_grants():


# Insert of role and privileges in Grants table
    insert_without_integrity_check("insert into GRANTS values (1,'Role','Basic user','')")
    insert_without_integrity_check("insert into GRANTS values (2,'Role','Moderator','')")
    insert_without_integrity_check("insert into GRANTS values (3,'Role','Administrator','')")
    insert_without_integrity_check("insert into GRANTS values (4,'Privilege','Create his Profile','')")
    insert_without_integrity_check("insert into GRANTS values (5,'Privilege','Update his Profile','')")
    insert_without_integrity_check("insert into GRANTS values (6,'Privilege','Delete his Profile','')")
    insert_without_integrity_check("insert into GRANTS values (7,'Privilege','Create his Pearl','')")
    insert_without_integrity_check("insert into GRANTS values (8,'Privilege','Update his Pearl','')")
    insert_without_integrity_check("insert into GRANTS values (9,'Privilege','Delete his Pearl','')")
    insert_without_integrity_check("insert into GRANTS values (10,'Privilege','Create his Comment','')")
    insert_without_integrity_check("insert into GRANTS values (11,'Privilege','Update his Comment','')")
    insert_without_integrity_check("insert into GRANTS values (12,'Privilege','Delete his Comment','')")
    insert_without_integrity_check("insert into GRANTS values (13,'Privilege','Reaction with a Smiley','')")
    insert_without_integrity_check("insert into GRANTS values (14,'Privilege','Update his Reaction','')")
    insert_without_integrity_check("insert into GRANTS values (15,'Privilege','Delete his Reaction','')")
    insert_without_integrity_check("insert into GRANTS values (16,'Privilege','Delete one Perle','')")
    insert_without_integrity_check("insert into GRANTS values (17,'Privilege','Delete one Comment','')")
    insert_without_integrity_check("insert into GRANTS values (18,'Privilege','Give a role','')")
    insert_without_integrity_check("insert into GRANTS values (19,'Privilege','Delete a role','')")
    insert_without_integrity_check("insert into GRANTS values (20,'Privilege','Delete one user','')")
    insert_without_integrity_check("insert into GRANTS values (21,'Privilege','Ban User','')")
    insert_without_integrity_check("insert into GRANTS values (22, 'Privilege','API Access','')")

# Insert of role and privileges in Grants table
# Table ASSO_GRANTS Load
# Role links
    insert_without_integrity_check("insert into Association_Grant values (2, 1)")
    insert_without_integrity_check("insert into Association_Grant values (3, 2)")

# Privilege links
## Basic User
    insert_without_integrity_check("insert into Association_Grant values (1, 4)")
    insert_without_integrity_check("insert into Association_Grant values (1, 5)")
    insert_without_integrity_check("insert into Association_Grant values (1, 6)")
    insert_without_integrity_check("insert into Association_Grant values (1, 7)")
    insert_without_integrity_check("insert into Association_Grant values (1, 8)")
    insert_without_integrity_check("insert into Association_Grant values (1, 9)")
    insert_without_integrity_check("insert into Association_Grant values (1, 10)")
    insert_without_integrity_check("insert into Association_Grant values (1, 11)")
    insert_without_integrity_check("insert into Association_Grant values (1, 12)")
    insert_without_integrity_check("insert into Association_Grant values (1, 13)")
    insert_without_integrity_check("insert into Association_Grant values (1, 14)")
    insert_without_integrity_check("insert into Association_Grant values (1, 15)")

## Moderator
    insert_without_integrity_check("insert into Association_Grant values (2, 16)")
    insert_without_integrity_check("insert into Association_Grant values (2, 17)")

## Administator
    insert_without_integrity_check("insert into Association_Grant values (3, 18)")
    insert_without_integrity_check("insert into Association_Grant values (3, 19)")
    insert_without_integrity_check("insert into Association_Grant values (3, 20)")
    insert_without_integrity_check("insert into Association_Grant values (3, 21)")
    insert_without_integrity_check("insert into Association_Grant values (3, 22)")


load_static_grants()

"""
*** Create admin user if not exist
"""
retunAdminQuery = db.session.query(User).filter_by(username='Admin').count()
if retunAdminQuery == 0:
    user_admin = User(username='Admin', password=generate_password_hash('chbtfybj5nj'))
    db.session.add(user_admin)
    roleAdmin = db.session.query(Grant).filter_by(name_grant='Administrator').first()
    asso_user = AssoUser(user_id=user_admin.id, granted_id=roleAdmin.id)
    db.session.add(asso_user)
    db.session.commit()

#

toto = db.session.query(User).filter_by(username='Admin').first()
pprint(toto.get_privilege_user())
