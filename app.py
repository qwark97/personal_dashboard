from config import App
from models import User

app = App.app
db = App.db

@app.route('/')
def home():
    return 'Home page'

@app.route('/create')
def create():
    user = User(
        name = 'Marcin',
        surname = 'Plata',
        email = 'test@mail.com',
        password = '123qwe'
    )
    db.session.add(user)
    db.session.commit()
    return 'User created'

if __name__ == "__main__":
    app.run(debug=True)