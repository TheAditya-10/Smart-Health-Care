from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.secret_key = 'my_super_secret_key_12345'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Adi!1%40T@localhost/smart_health_care'
#SQLALCHEMY_DATABASE_URI: Specifies the connection string to the database in the format

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Flask
#SQLALCHEMY_TRACK_MODIFICATIONS: Disables a feature that tracks object changes, improving performance.

db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

def predict_disease(symptoms, weight, height):
    # ML Model
    return "Disease A", 0.8


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = None

    if request.method == "POST":
        data = request.get_json()
        user_id = data.get('user_id')
        symptoms = data.get('symptoms')
        weight = data.get('weight')
        height = data.get('height')

        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'USER NOT FOUND'}), 404
        
        disease_name, probability = predict_disease(symptoms, weight, height)
        
        disease = Disease.query.filter_by(disease_name=disease_name).first()
        if not user:
            return jsonify({'error': 'DISEASE NOT FOUND'}), 404
        
        prediction = DiseasePrediction(user_id=user_id, disease_id = disease.disease_id, predicted_probability = probability)
        db.session.add(prediction)
        db.session.commit()

        return jsonify({
            'user_id': user_id,
            'predicted_disease': disease_name,
            'probability': probability
        })
    return render_template('predict.html', prediction = prediction)

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
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", 'danger')
    return render_template('login.html')

@app.route('/home')
def user_home():
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)