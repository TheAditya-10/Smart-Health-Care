from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model = "gemini-1.5-pro")

def predict_disease(symptoms, weight, height, gender, age):
    """Takes symptoms and health conditions, then predicts disease and suggests precautions."""
    prompt = f"""
    Symptoms: {symptoms}
    Weight: {weight} kg
    Height: {height} cm
    Gender: {gender}
    Age: {age} years
    Provide the two things:
    1. What is the probable disease that could be to this person and which type of disease is this.
    2. What should he/she should do now ? Give First hand precations.
    """
    response = model.invoke(prompt)
    return response.content

