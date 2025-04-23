from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from bot import predict_disease
from flask_sqlalchemy import SQLAlchemy
from models import *
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = 'my_super_secbhbsy_secret_key_12345'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("MYSQL_DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    full_name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Symptom(db.Model):
    __tablename__ = 'symptoms'
    symptom_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symptom_name = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        data = request.get_json()
        symptoms = data.get('symptoms')

        if not all([symptoms]):
            return jsonify({'error': 'INVALID REQUEST'}), 400
        
        if "user_id" in session:
            user = User.query.filter_by(user_id=session['user_id']).first()
            if user:
                weight = user.weight
                height = user.height
                age = user.age
                gender = user.gender
            else:
                return jsonify({'error': 'User not found'}), 404
        print(symptoms, weight, height, age, gender)
        precautions = predict_disease(symptoms, weight, height, gender, age)
        print(precautions)
        try:
            return jsonify({'generated_text': precautions})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return render_template('predict.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        full_name = request.form['full_name']
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        gender = request.form['gender']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate passwords
        if password != confirm_password:
            return "Passwords do not match!"

        # Hash the password
        hashed_password = generate_password_hash(password)
        user = User.query.filter_by(email=email).first()
        if user:
            return "Email already exists!"
        
        user = User.query.filter_by(username=username).first()
        if user:
            return "Username already exists!"
        
        new_user = User(
            username=username,
            email = email,
            full_name = full_name,
            age = age,
            weight = weight,
            height = height,
            gender = gender,
            password_hash = hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.user_id
            session['username'] = user.username
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", 'danger')
    return render_template('login.html')

if __name__ == '__main__':
    app.run()