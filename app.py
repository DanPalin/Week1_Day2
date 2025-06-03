from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100))
    name = db.Column(db.String(100))
    birthday = db.Column(db.Date)
    address = db.Column(db.String(200))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    def age(self):
        today = datetime.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('Users/login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()

    if user:
        session['user_id'] = user.id
        return redirect(url_for('profile'))
    else:
        return "Login failed. Invalid username or password."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        image_file = request.files['image']
        filename = secure_filename(image_file.filename)
        image_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"
        image_file.save(image_path)

        name = request.form['name']
        birthday = datetime.strptime(request.form['birthday'], '%Y-%m-%d')
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            return "Registration failed: Username already exists."

        user = User(
            image=filename,
            name=name,
            birthday=birthday,
            address=address,
            username=username,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('Users/register.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    user = User.query.get(session['user_id'])
    return render_template('Users/profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
