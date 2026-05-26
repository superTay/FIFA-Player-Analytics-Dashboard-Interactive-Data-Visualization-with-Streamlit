# create_dummy_model.py
"""
Trains a linear regression model to predict a player's 'potential'
and saves it to assets/model_fifa.pkl.
"""

from pathlib import Path
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

DATA_PATH = Path("data/players_21.csv")
ASSETS = Path("assets")
MODEL_PATH = ASSETS / "model_fifa.pkl"

# Must stay in sync with modules/page_model_inference.py. 'potential' is the
# target, so it is intentionally not a feature (would be label leakage).
FEATURES = ["age", "height_cm", "overall", "value_eur", "wage_eur"]
TARGET = "potential"


def build_model(data_path: Path = DATA_PATH, model_path: Path = MODEL_PATH) -> LinearRegression:
    """Train the regression model from the dataset and persist it to disk."""
    df = pd.read_csv(data_path)

    X = df[FEATURES].fillna(0)
    y = df[TARGET].fillna(df[TARGET].median())

    model = LinearRegression()
    model.fit(X, y)

    model_path.parent.mkdir(exist_ok=True)
    joblib.dump(model, model_path)
    return model


if __name__ == "__main__":
    build_model()
    print(f"✅ Model saved to {MODEL_PATH.resolve()}")
