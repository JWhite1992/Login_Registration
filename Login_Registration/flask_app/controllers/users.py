from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.model.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/sign_up',methods=['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    users ={ 
        "name": request.form['name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    users_id = User.save(users)
    session['user_id'] = users_id
    return redirect('/account_page')

@app.route('/log_in', methods=['POST'])
def login():
    users = User.get_email(request.form)
    if not users:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(users.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['users_id'] = users.id
    return redirect('/account_page')

@app.route('/account_page')
def dashboard():
    if 'users_id' not in session:
        return redirect('/logout')
    users ={
        'id': session['users_id']
    }
    return render_template("your_account.html", user =User.get_id(users))

@app.route('/sign_out')
def sign_out():
    session.clear()
    return redirect('/')