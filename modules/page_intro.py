# modules/page_intro.py
"""
Page 1: Introduction, data loading, and cleaning.

- Loads FIFA dataset from local CSV.
- Cleans and prepares data for visualization.
- Displays dataset overview and HTML description.
"""

import streamlit as st
import pandas as pd
from pathlib import Path


def show():
    """Render the Introduction page with local dataset loading, cleaning, and summary."""

    st.title("🏁 FIFA Player Analytics Dashboard ⚽")
    st.write("""
    This project analyzes FIFA player statistics, allowing users to explore,
    filter, and visualize data related to player performance and attributes.
    """)

    # --- LOCAL DATASET PATH ---
    DATA_PATH = "./data/players_21.csv"
    st.markdown("📂 **Data source:** Local file (`./data/players_21.csv`)")

    # --- DATA LOADING + CLEANING ---
    @st.cache_data
    def get_data(path: str) -> pd.DataFrame:
        """Load and clean the FIFA dataset (cached)."""
        df = pd.read_csv(path)
        df = clean_data(df)
        return df

    # --- CLEANING FUNCTION ---
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess the FIFA dataset.

        Steps:
        1. Drop unnecessary or redundant columns.
        2. Handle missing values.
        3. Convert data types.
        4. Standardize categorical variables if needed.
        """
        # 1️⃣ Drop unneeded columns
        cols_to_drop = [
            "player_url", "sofifa_id", "nation_logo_url", "club_logo_url",
            "club_flag_url", "player_face_url"
        ]
        df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors="ignore")

        # 2️⃣ Handle missing values
        # Fill numeric NaNs with median and categorical with 'Unknown'
        num_cols = df.select_dtypes(include=["int64", "float64"]).columns
        cat_cols = df.select_dtypes(include=["object"]).columns

        df[num_cols] = df[num_cols].fillna(df[num_cols].median())
        df[cat_cols] = df[cat_cols].fillna("Unknown")

        # 3️⃣ Convert types
        if "dob" in df.columns:
            df["dob"] = pd.to_datetime(df["dob"], errors="coerce")

        # Convert some relevant columns to category
        for col in ["nationality", "club_name", "preferred_foot", "player_positions"]:
            if col in df.columns:
                df[col] = df[col].astype("category")

        # 4️⃣ Rename columns (snake_case)
        df.columns = (
            df.columns
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )

        return df

    # --- LOAD DATA (cached) ---
    if "df" not in st.session_state:
        with st.spinner("Loading and cleaning dataset..."):
            st.session_state["df"] = get_data(DATA_PATH)
        st.success("✅ Local player data successfully cleaned and loaded!")

    df = st.session_state["df"]

    # --- DATA PREVIEW ---
    st.subheader("📋 Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    # --- STATS ---
    with st.expander("📊 Dataset Information"):
        st.write(f"**Rows:** {df.shape[0]}")
        st.write(f"**Columns:** {df.shape[1]}")
        st.write("**Column names (first 15):**")
        st.write(df.columns.tolist()[:15])

    # --- HTML DESCRIPTION ---
    show_html_description("./assets/dataset_description.html")


def show_html_description(html_path: str):
    """Render dataset description HTML if available."""
    html_file = Path(html_path)
    if html_file.exists():
        st.subheader("🧾 Dataset Description")
        st.components.v1.html(html_file.read_text(), height=400, scrolling=True)
    else:
        st.info("ℹ️ Dataset description file not found (`dataset_description.html`).")
