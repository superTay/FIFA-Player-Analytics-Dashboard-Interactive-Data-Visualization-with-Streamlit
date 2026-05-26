# modules/page_model_inference.py
"""
Page 3: Predictive Model — FIFA player potential estimation.

Loads a pre-trained regression model (training it on first run if the artifact
is missing) and predicts a player's potential from input attributes.
"""

import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

from create_dummy_model import FEATURES, MODEL_PATH, build_model


@st.cache_resource
def load_model():
    """Load the model, training it from the dataset on first run if missing."""
    if not MODEL_PATH.exists():
        build_model()
    return joblib.load(MODEL_PATH)


def show():
    """Render the Predictive Model page."""

    st.header("🤖 Predictive Model — FIFA Player Potential Estimation")

    if "df" not in st.session_state or st.session_state["df"].empty:
        st.warning("⚠️ Please start from the Introduction page to load the dataset.")
        return

    with st.spinner("Loading model..."):
        model = load_model()
    st.success("✅ Model loaded successfully!")

    # --- USER INPUT SECTION ---
    st.subheader("⚙️ Enter Player Attributes")

    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.slider("Age", 16, 45, 25)
        height_cm = st.number_input("Height (cm)", 150, 210, 180)
    with col2:
        overall = st.slider("Overall Rating", 40, 99, 75)
    with col3:
        value_eur = st.number_input("Market Value (€)", 0, 150_000_000, 10_000_000)
        wage_eur = st.number_input("Weekly Wage (€)", 0, 500_000, 50_000)

    # Built in FEATURES order so the columns match the trained model.
    input_data = pd.DataFrame(
        {
            "age": [age],
            "height_cm": [height_cm],
            "overall": [overall],
            "value_eur": [value_eur],
            "wage_eur": [wage_eur],
        }
    )[FEATURES]

    st.markdown("#### 🧾 Input Data")
    st.dataframe(input_data)

    # --- INFERENCE BUTTON ---
    if st.button("🔮 Predict Potential"):
        with st.spinner("Running model inference..."):
            prediction = model.predict(input_data)
        st.success(f"🎯 **Predicted Potential:** {prediction[0]:.2f}")

    st.markdown("---")
    st.caption("Scikit-learn LinearRegression trained on: " + ", ".join(FEATURES))
