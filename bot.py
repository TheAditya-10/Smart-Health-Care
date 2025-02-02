import google.generativeai as genai

# Set your Google Gemini API key
genai.configure(api_key="AIzaSyBhJnZmtfZP8j6WCosAeJebzIs3jqVZig4")

def predict_disease(symptoms, conditions):
    """Takes symptoms and health conditions, then predicts disease and suggests precautions."""
    prompt = f"I have these symptoms: {symptoms}. I also have these health conditions: {conditions}. What disease might I have? Suggest first-hand precautions."

    # Use Gemini AI model
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return response.text  # Get response as text

# Example usage
symptoms = "fever, cough, sore throat"
conditions = "diabetes"
result = predict_disease(symptoms, conditions)

print("AI Prediction:\n", result)
