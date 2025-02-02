from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from models import *
import torch

app = Flask(__name__)
app.secret_key = 'my_super_secbhbsy_secret_key_12345'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Adi!1%40T@localhost/smart_health_care'
#SQLALCHEMY_DATABASE_URI: Specifies the connection string to the database in the format

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Flask
#SQLALCHEMY_TRACK_MODIFICATIONS: Disables a feature that tracks object changes, improving performance.

#db = SQLAlchemy(app)

@app.route('/')
def home():
    return render_template('index.html')

model_name = 'gpt2'
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name)

# def predict_disease(symptoms, weight, height):
#     prompt = f"""
#     Symptoms: {symptoms}
#     Weight: {weight} kg
#     Height: {height} cm
#     Provide the two things:
#     1. What is the probable disease that could be to this person and which type of disease is this.
#     2. What should he/she should do now ? First hand precations.
#     """
#     try:
#         input_ids = tokenizer.encode(prompt, return_tensors='pt')
#         output = model.generate(input_ids, max_length=200, temperature = 0.7, pad_token_id=tokenizer.eos_token_id)
#         generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
#         #lines = generated_text.split('\n')
#         #disease = lines # if len(lines) > 1 else "Unknown Disease"
#         #precautions = lines #[1] if len(lines) > 1 else "Unknown Precautions"

#         return generated_text
    
#     except Exception as e:
#         return "Error", str(e)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == "POST":
        data = request.get_json()
        symptoms = data.get('symptoms')
        weight = data.get('weight')
        height = data.get('height')

        if not all([symptoms, weight, height]):
            return jsonify({'error': 'INVALID REQUEST'}), 400

        try:
            disease, precautions = predict_disease(symptoms, weight, height)
            if disease[0] == "Error":
                return jsonify({'error': disease[1]}), 500

            return jsonify({
                'predicted_disease': disease,
                'precautions': precautions,
            })
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

@app.route('/home')
def user_home():
    return render_template('home.html')

if __name__ == '__main__':
#    with app.app_context():
 #       db.create_all()
    app.run(debug=True)