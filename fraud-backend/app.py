from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

# Initialize app
app = Flask(__name__)
# Configure CORS to allow your Vercel domain
CORS(app, origins=[
    "https://creditcardfraud-git-main-ovee-manolkars-projects.vercel.app",
    "http://localhost:3000"  # For local development
])

# Load pipeline (classifier included inside)
pipeline = joblib.load("business_pipeline.pkl")

# Define expected fields
expected_fields = ["Amount", "Country", "TimeOfDay", "MerchantType"]

@app.route("/")
def home():
    return "✅ Credit Card Fraud Detection API is running"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        
        # Check if all fields are present
        if not all(field in data for field in expected_fields):
            return jsonify({"error": f"Missing one of the required fields: {expected_fields}"}), 400

        # Create DataFrame from input
        input_df = pd.DataFrame([{
            "Amount": float(data["Amount"]),
            "Country": data["Country"],
            "TimeOfDay": data["TimeOfDay"],
            "MerchantType": data["MerchantType"]
        }])

        # Predict directly from pipeline
        prediction = pipeline.predict(input_df)[0]
        result = "Fraud" if prediction == -1 else "Normal"

        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
