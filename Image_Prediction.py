import requests

# Define the Flask server URL
URL = "http://127.0.0.1:5000/predict"  # Ensure Flask server is running

# Set the image filename
img_filename = "Test/5.png"  # Change this to your actual image file

try:
    # Open and send the image file
    with open(img_filename, "rb") as img_file:
        files = {'file': img_file}  # Flask expects a 'file' key
        response = requests.post(URL, files=files)

    # Print server response
    if response.status_code == 200:
        print("Prediction:", response.json())  # Corrected to print the whole JSON response
    else:
        print("Error:", response.json())

except Exception as e:
    print("Error loading file:", e)
