from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, EqualTo
from flask_mysqldb import MySQL
import yaml
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

db = yaml.load(open('db.yaml'))
app = Flask(__name__)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_pwd']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['SECRET_KEY'] = '89362483764bd74638763478634'
bootstrap = Bootstrap(app)
mysql = MySQL(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

class RegistrationForm(FlaskForm):
    companyName = StringField('Company Name', validators=[DataRequired()])
    managerName = StringField('Manager Name', validators=[DataRequired()])
    # companyType = SelectField('Business Type', choices=[])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    companyName = StringField('Company Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')

class userRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class userLoginForm(FlaskForm):
    username = StringField('Userame', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')

@app.route("/")
def index():
    return render_template('/index.html')

@app.route("/business")
def b_index():
    return render_template('/business/b_index.html')

@app.route("/user")
def u_index():
    return render_template('/user/u_index.html')

@app.route('/business/signup', methods=['GET', 'POST'])
def b_signup():
    form = RegistrationForm()
    cur = mysql.connection.cursor()
    count = cur.execute('select business_type_name from business_type')
    if count > 0:
        businessTypes = cur.fetchall()
        # form.companyType.choices = cur.fetchall()
        cur.close()
    if request.method == "POST":
        companyDetails = request.form
        companyName = companyDetails['companyName']
        managerName = companyDetails['managerName']
        companyType = companyDetails.get('businessType')
        password = generate_password_hash(companyDetails['password'])
        cur = mysql.connection.cursor()
        cur.execute('select business_type_id from business_type where business_type_name=%s', (companyType,))
        cur.execute('insert into businesses(business_name, manager_name, business_type_id, business_pwd)'
                    'values(%s, %s, %s, %s)', (companyName, managerName, cur.fetchall()[0][0], password))
        mysql.connection.commit()
        cur.close()
        return 'Success'
    return render_template('/business/b_signup.html', form=form, businessTypes=businessTypes)

@app.route('/business/login', methods=['GET', 'POST'])
def b_login():
    form = LoginForm()
    if request.method == "POST":
        companyDetails = request.form
        companyName = companyDetails['companyName']
        password = companyDetails['password']
        cur = mysql.connection.cursor()
        user = cur.execute('select business_pwd from businesses where business_name=%s', (companyName,))
        pwd = cur.fetchall()[0][0]
        cur.close()
        if user > 0:
            if check_password_hash(pwd, password):
                return 'Success'
            else:
                return '<h1>Invalid username or password</h1>'
    return render_template('/business/b_login.html', form=form)


@app.route('/user/signup', methods=['GET', 'POST'])
def u_signup():
    form = userRegistrationForm()
    if request.method == "POST":
        userDetails = request.form
        username = userDetails['username']
        password = generate_password_hash(userDetails['password'])
        cur = mysql.connection.cursor()
        cur.execute('insert into users(user_name, user_pwd) values(%s, %s)', (username, password))
        mysql.connection.commit()
        cur.close()
        return 'Success'
    return render_template('/user/u_signup.html', form=form)

@app.route('/user/login', methods=['GET', 'POST'])
def u_login():
    form = userLoginForm()
    if request.method == "POST":
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        cur = mysql.connection.cursor()
        user = cur.execute('select user_pwd from users where user_name=%s', (username,))
        pwd = cur.fetchall()[0][0]
        cur.close()
        if user > 0:
            if check_password_hash(pwd, password):
                return 'Success'
            else:
                return '<h1>Invalid username or password</h1>'
    return render_template('/user/u_login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)