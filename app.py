from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, login_required, current_user, logout_user
from config import App
from models import User, Note
from helpers import get_weather, validate_name, validate_pass, validate_email
from werkzeug import generate_password_hash, check_password_hash
import datetime

app = App.app
db = App.db
login_manager = App.login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')
    
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password_check = request.form.get('password_check')

    user = User.query.filter_by(email=email).first() 

    if password != password_check:
        flash('Both passwords must be the same')
        return redirect(url_for('signin'))
    if user: 
        flash('User already exists')
        return redirect(url_for('signin'))

    if not validate_email(email):
        flash('E-mail address is not valid')
        return redirect(url_for('signin'))

    if not validate_pass(name):
        flash('Password is not valid')
        return redirect(url_for('signin'))

    if not validate_name(name):
        flash('Name name must be between 4 and 20 characters lenght')
        return redirect(url_for('signin'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    flash('User has been created')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('Please type login and password.')
        return redirect(url_for('login'))

    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first() 
    if not user:
        flash('There is no such user.')
        return redirect(url_for('login'))
    
    if not check_password_hash(user.password, password):
        flash('Please check user and password again.')
        return redirect(url_for('login'))

    login_user(user, remember=remember)

    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out')
    return redirect(url_for('login'))

@app.route('/')
@app.route('/home')
@login_required
def home():
    summary, temp = get_weather()
    return render_template('home.html', summary=summary, temp=temp)

@app.route('/notes', methods=['GET', 'POST', 'PUT'])
@login_required
def notes():
    summary, temp = get_weather()
    notes_object = []
    user_id = current_user.id

    if request.method == 'POST':
        content = request.form.get('new-note').strip()
        new_note = Note(content=content, user_id=user_id, date=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'))
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('notes'))

    notes_objects = User.query.filter_by(id=user_id).first().notes
    return render_template('notes.html', summary=summary, temp=temp, notes=sorted(notes_objects, key=lambda x: x.date))

@app.route('/update_note', methods=['POST'])
@login_required
def update_note():
    user_id = current_user.id
    new_content = request.form.get('edited-note').strip()
    note_id = request.form.get('note-id')
    old_note = Note.query.filter_by(id=note_id).first()
    old_note.content = new_content
    old_note.date = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    db.session.commit()
    return redirect(url_for('notes'))

@app.route('/delete_note', methods=['POST'])
@login_required
def delete_note():
    user_id = current_user.id
    note_id = request.form.get('note-id')
    old_note = Note.query.filter_by(id=note_id).first()
    db.session.delete(old_note)
    db.session.commit()
    return redirect(url_for('notes'))

@app.route('/money')
@login_required
def money():
    pass

@app.route('/commitments')
@login_required
def commitments():
    pass

@app.route('/receivable')
@login_required
def receivable():
    pass

@app.route('/friends')
@login_required
def friends():
    pass

@app.route('/pictures')
@login_required
def pictures():
    pass

@app.route('/portfolio')
@login_required
def portfolio():
    pass

with app.test_request_context():
    url_for('home')
    url_for('login')
    url_for('signin')

if __name__ == "__main__":
    app.run(debug=True)

