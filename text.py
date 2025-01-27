import openai

# Set your API key
openai.api_key = "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"

try:
    # Test with a simple API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}]
    )
    print("API key is working!")
    print("Response:", response.choices[0].message['content'])
except openai.error.AuthenticationError:
    print("Invalid API key! Please check and try again.")
except openai.error.OpenAIError as e:
    print(f"API key is not working. Error: {e}")
