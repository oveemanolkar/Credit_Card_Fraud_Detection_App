from flask import Flask, request, jsonify
from flask_cors import CORS   # ✅ Add this
import joblib
import pandas as pd

app = Flask(__name__)
CORS(app)  # ✅ Allow all origins (later you can restrict to Vercel domain)

# Load the trained pipeline
pipeline = joblib.load("business_pipeline.pkl")

@app.route('/')
def home():
    return "✅ Credit Card Fraud Detection API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_df = pd.DataFrame([data])
        prediction = pipeline.predict(input_df)[0]
        return jsonify({
            "prediction": int(prediction),
            "message": "Fraud" if prediction == 1 else "Not Fraud"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
