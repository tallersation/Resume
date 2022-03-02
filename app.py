#Dev by : Thiarasak Khamyan
#1st Edited : 1 Mar 2022 (Midnight)


from re import U
from sqlalchemy.orm import query
from flask import Flask, render_template, url_for, redirect, jsonify, json, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.validators import Length, DataRequired
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


#Config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.debug = True

db = SQLAlchemy(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


#Database
class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password_hash = password

class List(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    paid_status = db.Column(db.String(50), nullable=False, unique=False)
    date = db.Column(db.Date(), nullable=False, unique=False)
    total = db.Column(db.Integer, nullable=False, unique=False)
    reason = db.Column(db.String(100), nullable=True, unique=False)


    def __init__(self, status, date, total, reason):
        self.paid_status = status
        self.date = date
        self.total = total
        self.reason = reason

#Forms
class Forms(FlaskForm):
    date = DateTimeField(label='Date', validators=[DataRequired()])
    total = StringField(label='Total', validators=[DataRequired()])
    reason = StringField(label='Reason', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

class Login(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = StringField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Login")


#Route
@login_manager.user_loader
def load_user(id):
    return Account.query.get(int(id))

@login_manager.unauthorized_handler
def handle_needs_login():
    flash("ล็อคอินก่อนเด้อ.....")
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('login'))
    
@app.route('/login-query', methods=['GET', 'POST'])
def query():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True
    user_log = Account.query.filter_by(username=username).first()

    if not user_log and not check_password_hash(user_log.password_hash, password):
        flash("แยงผ่อ เมล กับ รหัส ใหม่เด้อ")
        return redirect(url_for('login'))

    login_user(user_log, remember=remember)
    return redirect(url_for('account'))
        
@app.route('/account')
@login_required
def account():
    return


@app.route('/json_reg', methods=['POST'])
def json_rev():
    postJson = request.get_json()
    name = postJson['name']
    username = postJson['username']
    password = postJson['pwd']
    user_reg = Account.query.filter_by(username=username).first()
    if user_reg:
        return jsonify({
            'Success' : False,
            'Error' : "เช็คไอดีแหมรอบเด้อ..."
        })
    user_to_create = Account(
        name = name,
        username = username,
        password = generate_password_hash(password, method='sha256')
    )
    db.session.add(user_to_create)
    db.session.commit()
    return jsonify({
        'Success' : True,
        'Error' : "สมัครสมาชิกเรียบแล้วแล้วเด้อ...."
    })

# @app.route('/status', methods=['POST'])
# def status_post():
#     postJson = request.get_json()
#     status = "online"
#     if postJson:
#         status = postJson['status']
#         session['status'] = status
#     return jsonify(status)

if __name__ == '__main__':
    app.run()