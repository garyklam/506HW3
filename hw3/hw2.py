from flask import Flask, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_login import current_user, login_user, login_required, logout_user
from models import db, login, UserModel


class loginForm(FlaskForm):
	username = StringField(label='Username',validators=[DataRequired(), Length(min=5, max=20)])
	password = PasswordField(label='Password',validators=[DataRequired(), Length(min=6,max=16)])
	submit = SubmitField(label='Login')

class registerForm(FlaskForm):
	username = StringField(label='Username',validators=[DataRequired(), Length(min=5, max=20)])
	password = PasswordField(label='Password',validators=[DataRequired(), Length(min=6,max=16)])
	checkpassword = PasswordField(label="Re-Enter Password",validators=[DataRequired(), EqualTo('password', message="Passwords do not match")])
	email = StringField(label='Email',validators=[DataRequired(), Email()])
	submit = SubmitField(label="Register")
	
app=Flask(__name__)
app.secret_key='a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)
login.login_view = 'login'
 	
@app.before_first_request
def create_table():
	db.create_all()
    
@app.route('/')
def baseSite():
	return redirect("/login")
    
@app.route('/homepage')
@login_required  
def homepage():
	return render_template('home.html')

@app.route('/login',methods=["POST", "GET"])
def login():
	if current_user.is_authenticated:
		return redirect('/homepage')
	form=loginForm()
	if form.validate_on_submit():
		if request.method == "POST":
			username=request.form["username"]
			pw=request.form["password"]
			user = UserModel.query.filter_by(username = username).first()
			if user and user.check_password(pw):
				login_user(user)
				return redirect('/homepage')
			else:
				flash("Invalid Login Details")
				return redirect('/login')
		else:
        		return render_template('login.html',form=form)
	else:
		return render_template('login.html',form=form)


@app.route('/register',methods=["POST", "GET"])
def register():
	form = registerForm()
	if form.validate_on_submit():
		if request.method == "POST":
			username=request.form["username"]
			pw=request.form["password"]
			email=request.form["email"]
			user = UserModel.query.filter_by(username = username).first()
			address = UserModel.query.filter_by(email = email).first()
			if user:
				flash("Username already exists.")
				return redirect('/register')
			elif address:
				flash("Email already in use.")
				return redirect('/register')
			else:
				new_user = UserModel(username=username)
				new_user.set_password(pw)
				new_user.email=email
				db.session.add(new_user)
				db.session.commit()
				return redirect('/login')
		else:
			return render_template('registration.html', form=form)
	else:
		return render_template('registration.html', form=form)
				
@app.route('/logout')
def logout():
	logout_user()
	return redirect('/login')
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
