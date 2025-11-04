# modules/page_model_inference.py
"""
Page 3: Predictive Model — Demo for AI model inference (pre-trained example).

This page simulates loading a pre-trained model (from file) and allows the user
to make predictions on selected player attributes.
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib  # For loading the pre-trained model
from pathlib import Path


@st.cache_resource
def load_model():
    model_path = Path("assets/model_fifa.pkl")
    return joblib.load(model_path)


def show():
    """Render the Predictive Model page."""

    st.header("🤖 Predictive Model — FIFA Player Potential Estimation")

    # --- LOAD DATA FROM SESSION ---
    if "df" not in st.session_state or st.session_state["df"].empty:
        st.warning("⚠️ Please start from the Introduction page to load the dataset.")
        return

    df = st.session_state["df"]

    # --- LOAD MODEL (pre-trained externally) ---
    model_path = Path("assets/model_fifa.pkl")

    if not model_path.exists():
        st.error("❌ Model file not found! Please ensure 'model_fifa.pkl' is in the assets/ directory.")
        st.info("You can simulate a model by creating one using scikit-learn and saving it with joblib.dump().")
        return

    with st.spinner("Loading model..."):
        model = joblib.load(model_path)

    st.success("✅ Model loaded successfully!")

    # --- USER INPUT SECTION ---
    st.subheader("⚙️ Enter Player Attributes")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Age", 16, 45, 25)
        height = st.number_input("Height (cm)", 150, 210, 180)
    with col2:
        overall = st.slider("Overall Rating", 40, 99, 75)
        potential = st.slider("Current Potential", 40, 99, 80)
    with col3:
        value_eur = st.number_input("Market Value (€)", 0, 150_000_000, 10_000_000)
        wage_eur = st.number_input("Weekly Wage (€)", 0, 500_000, 50_000)

    input_data = pd.DataFrame(
        {
            "age": [age],
            "height_cm": [height],
            "overall": [overall],
            "potential": [potential],
            "value_eur": [value_eur],
            "wage_eur": [wage_eur],
        }
    )

    st.markdown("#### 🧾 Input Data")
    st.dataframe(input_data)

    # --- INFERENCE BUTTON ---
    if st.button("🔮 Predict Future Potential"):
        with st.spinner("Running model inference..."):
            prediction = model.predict(input_data)
        st.success(f"🎯 **Predicted Future Potential:** {prediction[0]:.2f}")

    st.markdown("---")
    st.caption("Model loaded from assets/model_fifa.pkl — trained externally with Scikit-learn.")
