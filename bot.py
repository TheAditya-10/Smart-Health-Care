import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
client = genai.GenerativeModel("gemini-1.5-pro")
model = ChatGoogleGenerativeAI(client=client, temperature=0.5, max_output_tokens=1000)

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

