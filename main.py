from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa


app = Flask("test application")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite"
db = SQLAlchemy(app)


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    login = sa.Column(sa.Text, unique=True, nullable=False)
    password = sa.Column(sa.Text, nullable=False)


with app.app_context():
    db.create_all()


# GET
@app.route("/")
def name_of_func():
    return "OK 1"


@app.route("/qwerty")
def name_of_func_2():
    return "OK 2"


@app.post("/registration")
def registration():
    login = request.form.get("login")
    passwd = request.form.get("password")
    print(login, passwd)
    if not login or not passwd:
        return "No such data in request", 400
    check_user = User.query.filter_by(login=login).first()
    if check_user:
        return "login already exist", 400
    test_user = User(login=login, password=generate_password_hash(passwd))
    db.session.add(test_user)
    db.session.commit()
    return "OK"


@app.post("/auth")
def auth():
    login = request.form.get("login")
    passwd = request.form.get("password")
    print(login, passwd)
    if not login or not passwd:
        return "No such data in request", 400
    test = User.query.filter_by(login=login).first()
    if not test or not check_password_hash(test.password, passwd):
        return "login or password not match", 401
    return "success", 200


app.run(port=5001, debug=True)
