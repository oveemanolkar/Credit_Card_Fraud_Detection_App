import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Load the dataset
df = pd.read_csv("creditcard.csv")

# Simulate business-level features (replace with real if you have)
df["Amount"] = df["Amount"]
df["Country"] = np.random.choice(["US", "UK", "IN", "AU"], size=len(df))
df["TimeOfDay"] = np.random.choice(["morning", "afternoon", "evening", "night"], size=len(df))
df["MerchantType"] = np.random.choice(["online", "grocery", "travel", "electronics"], size=len(df))

# Use a small balanced subset for training (just for this demo)
fraud = df[df["Class"] == 1]
normal = df[df["Class"] == 0].sample(len(fraud) * 3, random_state=42)
data = pd.concat([fraud, normal])

X = data[["Amount", "Country", "TimeOfDay", "MerchantType"]]

# Create preprocessing pipeline
numeric = ["Amount"]
categorical = ["Country", "TimeOfDay", "MerchantType"]

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), numeric),
    ("cat", OneHotEncoder(), categorical)
])

# Define the model pipeline
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("clf", IsolationForest(contamination=0.1, random_state=42))
])

# Fit the model
model.fit(X)

# Save pipeline and model separately for API
joblib.dump(model.named_steps["clf"], "fraud_model.pkl")
joblib.dump(model.named_steps["preprocessor"], "business_pipeline.pkl")

print("✅ Model and pipeline saved.")
