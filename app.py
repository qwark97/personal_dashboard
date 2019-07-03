from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, login_required, current_user, logout_user
from config import App
from models import User, Note, Friend, Commitment, Receivable
from helpers import get_weather, validate_name, validate_pass, validate_email,flatten
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
    user_id = current_user.id
    friends_objects = User.query.filter_by(id=user_id).first().friends

    notes_objects = User.query.filter_by(id=user_id).first().notes

    all_receivables = flatten([friend.receivables for friend in friends_objects])
    all_commitments = flatten([friend.commitments for friend in friends_objects])

    money = True if all_receivables or all_commitments else False

    receivables = flatten([friend.receivables for friend in friends_objects])
    commitments = flatten([friend.commitments for friend in friends_objects])

    receivable_sum = round(sum(receivable.amount for receivable in all_receivables), 2)
    commitment_sum = round(sum(commitment.amount for commitment in all_commitments), 2)
    money_summary = round(abs(receivable_sum-commitment_sum), 2)

    sums=(receivable_sum, commitment_sum, money_summary)

    return render_template('home.html', 
                            summary=summary, 
                            temp=temp,
                            notes=notes_objects,
                            money=money,
                            receivables=receivables,
                            commitments=commitments,
                            sums=sums)

@app.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    summary, temp = get_weather()
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

@app.route('/friends', methods=['POST', 'GET'])
@login_required
def friends():
    summary, temp = get_weather()
    user_id = current_user.id

    if request.method == 'POST':
        name = request.form.get('new-friend').strip()
        new_friend = Friend(name=name, user_id=user_id)
        db.session.add(new_friend)
        db.session.commit()
        return redirect(url_for('friends'))

    friends_objects = User.query.filter_by(id=user_id).first().friends
    return render_template('friends.html', summary=summary, temp=temp, friends=sorted(friends_objects, key=lambda x: x.name))

@app.route('/update_friend', methods=['POST'])
@login_required
def update_friend():
    user_id = current_user.id
    new_name = request.form.get('edited-friend').strip()
    friend_id = request.form.get('friend-id')
    old_friend = Friend.query.filter_by(id=friend_id).first()
    old_friend.name = new_name
    db.session.commit()
    return redirect(url_for('friends'))

@app.route('/delete_friend', methods=['POST'])
@login_required
def delete_friend():
    user_id = current_user.id
    friend_id = request.form.get('friend-id')
    old_friend = Friend.query.filter_by(id=friend_id).first()
    db.session.delete(old_friend)
    db.session.commit()
    return redirect(url_for('friends'))

@app.route('/commitments', methods=['POST', 'GET'])
@login_required
def commitments():
    summary, temp = get_weather()
    user_id = current_user.id

    if request.method == 'POST':
        friend_id = request.form.get('friend_id')

        title = request.form.get('reason')
        try:
            amount = request.form.get('how-much').replace(',','.')
            amount = float(amount)
        except:
            flash('Enter valid amount!')
            return redirect(url_for('commitments'))
        new_commitment = Commitment(
            amount=amount,
            title=title,
            date=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            friend_id=friend_id)
        db.session.add(new_commitment)
        db.session.commit()
    

    friends_objects = User.query.filter_by(id=user_id).first().friends
    all_commitments = [(friend.name, friend.commitments, sum(commitment.amount for commitment in friend.commitments)) 
                      for friend in friends_objects]

    return render_template('commitments.html',
                            summary=summary, 
                            temp=temp, 
                            friends=friends_objects, 
                            all_commitments=all_commitments)

@app.route('/delete_commitment', methods=['POST'])
@login_required
def delete_commitment():
    user_id = current_user.id
    commitment_id = request.form.get('commitment-id')
    old_commitment = Commitment.query.filter_by(id=commitment_id).first()
    db.session.delete(old_commitment)
    db.session.commit()
    return redirect(url_for('commitments'))                       

@app.route('/receivables', methods=['POST', 'GET'])
@login_required
def receivables():
    summary, temp = get_weather()
    notes_object = []
    user_id = current_user.id

    if request.method == 'POST':
        friend_id = request.form.get('friend_id')

        title = request.form.get('reason')
        try:
            amount = request.form.get('how-much').replace(',','.')
            amount = float(amount)
        except:
            flash('Enter valid amount!')
            return redirect(url_for('receivables'))
        new_receivable = Receivable(
            amount=amount,
            title=title,
            date=datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            friend_id=friend_id)
        db.session.add(new_receivable)
        db.session.commit()
    

    friends_objects = User.query.filter_by(id=user_id).first().friends
    all_receivables = [(friend.name, friend.receivables, sum(receivable.amount for receivable in friend.receivables)) 
                      for friend in friends_objects]

    return render_template('receivables.html',
                            summary=summary, 
                            temp=temp, 
                            friends=friends_objects, 
                            all_receivables=all_receivables)

@app.route('/delete_receivable', methods=['POST'])
@login_required
def delete_receivable():
    user_id = current_user.id
    receivable_id = request.form.get('receivable-id')
    old_receivable = Receivable.query.filter_by(id=receivable_id).first()
    db.session.delete(old_receivable)
    db.session.commit()
    return redirect(url_for('receivables'))

@app.route('/pictures')
@login_required
def pictures():
    pass

@app.route('/portfolio')
@login_required
def portfolio():
    pass

if __name__ == "__main__":
    app.run(debug=True)

