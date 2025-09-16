import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Load dataset
df = pd.read_csv("creditcard.csv")

# 2. Feature engineering
# Map time (seconds) -> TimeOfDay
def get_time_of_day(t):
    hour = (t // 3600) % 24
    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    elif 18 <= hour < 24:
        return "evening"
    else:
        return "night"

df["TimeOfDay"] = df["Time"].apply(get_time_of_day)

# Add fake Country + MerchantType (for demo)
countries = ["US", "UK", "IN", "CA"]
merchant_types = ["online", "retail", "food", "travel"]

np.random.seed(42)
df["Country"] = np.random.choice(countries, len(df))
df["MerchantType"] = np.random.choice(merchant_types, len(df))

# 3. Select features + target
features = ["Amount", "Country", "TimeOfDay", "MerchantType"]
X = df[features]
y = df["Class"]

# 4. Preprocessor
numeric_features = ["Amount"]
numeric_transformer = StandardScaler()

categorical_features = ["Country", "TimeOfDay", "MerchantType"]
categorical_transformer = OneHotEncoder(handle_unknown="ignore")

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

# 5. Pipeline (Preprocessing + Classifier)
pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# 6. Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train
pipeline.fit(X_train, y_train)

# 7. Save pipeline
joblib.dump(pipeline, "business_pipeline.pkl")

print("✅ Model trained and saved as business_pipeline.pkl")
