import os
import io
import pickle
import json
import numpy as np
import faiss
import requests
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
from groq import Groq
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ========== TEXT Q&A SYSTEM ========== #

# Load Sentence Transformer model
model = SentenceTransformer('./Embed_Model/Sentence_Transformer/all-MiniLM-L6-v2')

# Load FAISS index
index = faiss.read_index("./Indexes_and_data/question_index.faiss")

# Load stored answers
with open('./Indexes_and_data/answers.pkl', 'rb') as f:
    answers = pickle.load(f)

def get_answer(user_question):
    """Retrieve the best answer using FAISS index."""
    user_embedding = model.encode([user_question]).astype('float32')
    faiss.normalize_L2(user_embedding)  # Normalize embedding
    D, I = index.search(user_embedding, k=1)  # FAISS search
    best_match_idx = I[0][0]  # Get best match
    return answers[best_match_idx]  # Return the answer

@app.route('/response', methods=['POST'])
def final_response():
    data = request.get_json()
    if not data or 'user_question' not in data:
        return jsonify({"error": "Missing 'user_question' in request"}), 400

    user_question = data['user_question']
    answer = get_answer(user_question)

    prompt = {
        'role': 'user',
        'content': f'''Instruction:
            1. If the question is not related to "Heart/Cardio" topics, respond with:
                "This is an Out of Scope Question. Please try again with cardiovascular/heart-related queries."
            2. Ensure the answer is relevant to the question with proper headings.
            3. Do not mention this prompt in your response.

            Question: {user_question}
            Answer: {answer}
        '''
    }

    # Set API Key for Groq
    os.environ["GROQ_API_KEY"] = "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"
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    
    chat_completion = client.chat.completions.create(
        messages=[prompt],
        model="llama-3.1-8b-instant",
    )

    res = chat_completion.choices[0].message.content
    return jsonify({"response": res})

from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input as preprocess_mobilenet

# ========== ECG IMAGE CLASSIFICATION ========== #

# Load trained MobileNet model
MODEL_PATH = "mobilenet_model_TF2_12.keras"
tf_model = load_model(MODEL_PATH, compile=False)

# Define class labels
class_names = ['Ventricular', 'Myocardial Infarction', 'Normal', 'Supraventricular', 'Unclassified']

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Preprocess the image
    img = image.load_img(io.BytesIO(file.read()), target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_mobilenet(x)

    # Make a prediction
    preds = tf_model.predict(x)
    class_idx = np.argmax(preds[0])
    class_label = class_names[class_idx]

    return jsonify({'prediction': class_label})

# Run Flask server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
