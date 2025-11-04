# create_dummy_model.py
"""
Creates a simple linear regression model to predict 'potential'
and saves it to assets/model_fifa.pkl.
"""

from pathlib import Path
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

# --- paths ---
DATA_PATH = Path("data/players_21.csv")
ASSETS = Path("assets")
ASSETS.mkdir(exist_ok=True)
MODEL_PATH = ASSETS / "model_fifa.pkl"

# --- load data ---
df = pd.read_csv(DATA_PATH)

# --- features/target (keep it simple for the demo) ---
X = df[["overall", "age", "value_eur"]].fillna(0)
y = df["potential"].fillna(df["potential"].median())

# --- train model ---
model = LinearRegression()
model.fit(X, y)

# --- save model ---
joblib.dump(model, MODEL_PATH)
print(f"✅ Model saved to {MODEL_PATH.resolve()}")
