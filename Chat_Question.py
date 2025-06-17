import requests

URL = "http://127.0.0.1:5000/response"

# Sample cardiovascular-related question
text = "I am a 39-year-old female. My heart rate is around 97-106 at rest, and my BP is 140/90. Should I be concerned?"

data = {"user_question": text}

response = requests.post(URL, json=data)
print(response)
if response.status_code == 200:
    print("Response:", response.json())  
else:
    print("Error:", response.json())

