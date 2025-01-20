from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Consultant(db.Model):
    __tablename__ = 'consultants'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    specialisation = db.Column(db.String(255), nullable = False)
    contact = db.Column(db.String(255), nullable = False)
    available_slots = db.Column(db.Text, nullable = False)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, nullable = False)
    consulatant_id = db.Column(db.Integer, db.ForeignKey('consultants.id'), nullable = False)
    slot = db.Column(db.String(255), nullable = False)
    booking_date = db.Column(db.Date, nullable = False)

    consultant = db.relationship('Consultant', backref= 'bookings')

# User Table: Stores patient details
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

# Symptom Table: Stores details of different diseases and symptoms
class Symptom(db.Model):
    __tablename__ = 'symptoms'
    symptom_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symptom_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

# Disease Table: Stores disease details with associated symptoms
class Disease(db.Model):
    __tablename__ = 'diseases'
    disease_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    disease_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    symptom_ids = db.Column(db.Text, nullable=True)  # Comma-separated list or JSON format of symptom_ids

# Disease Prediction Table: Stores predictions for each patient
class DiseasePrediction(db.Model):
    __tablename__ = 'disease_predictions'
    prediction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    disease_id = db.Column(db.Integer, db.ForeignKey('diseases.disease_id'), nullable=False)
    predicted_probability = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship for easier access
    user = db.relationship('User', backref=db.backref('disease_predictions'))
    disease = db.relationship('Disease', backref=db.backref('disease_predictions'))

# BMI Calculation Table: Stores BMI values for users (optional)
class BMICalculation(db.Model):
    __tablename__ = 'bmi_calculations'
    bmi_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    bmi_value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship for easier access
    user = db.relationship('User', backref=db.backref('bmi_calculations'))