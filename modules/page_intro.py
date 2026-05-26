# modules/page_intro.py
"""
Page 1: Introduction — data loading, cleaning, and descriptive overview.

- Initializes session state for persistence.
- Loads and cleans the FIFA dataset (cached).
- Displays preview, summary stats, and dataset dictionary.
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from pathlib import Path


def show():
    """Render the Introduction page with dataset info and cleaning."""

    st.title("🏁 FIFA Player Analytics Dashboard ⚽")
    st.write("""
    This project analyzes FIFA player statistics, allowing users to explore,
    filter, and visualize data related to player performance and attributes.
    """)

    # --- INITIALIZE SESSION STATE ---
    if "df" not in st.session_state:
        st.session_state["df"] = pd.DataFrame()  # ensure existence before any access

    # --- LOCAL DATASET PATH ---
    DATA_PATH = "./data/players_21.csv"
    st.markdown("📂 **Data source:** Local file (`./data/players_21.csv`)")

    # --- CACHED LOADING FUNCTION ---
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
        """
        # Drop unnecessary columns
        cols_to_drop = [
            "player_url", "sofifa_id", "nation_logo_url", "club_logo_url",
            "club_flag_url", "player_face_url"
        ]
        df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors="ignore")

        # Fill missing values
        num_cols = df.select_dtypes(include=["int64", "float64"]).columns
        cat_cols = df.select_dtypes(include=["object"]).columns
        df[num_cols] = df[num_cols].fillna(df[num_cols].median())
        df[cat_cols] = df[cat_cols].fillna("Unknown")

        # Convert date of birth
        if "dob" in df.columns:
            df["dob"] = pd.to_datetime(df["dob"], errors="coerce")

        # Convert categorical columns
        for col in ["nationality", "club_name", "preferred_foot", "player_positions"]:
            if col in df.columns:
                df[col] = df[col].astype("category")

        # Rename columns
        df.columns = (
            df.columns
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )

        return df

    # --- LOAD DATA INTO SESSION STATE ---
    if st.session_state["df"].empty:
        with st.spinner("Loading and cleaning dataset..."):
            st.session_state["df"] = get_data(DATA_PATH)
        st.success("✅ Local player data successfully cleaned and loaded!")

    df = st.session_state["df"]

    # --- EXPANDER 1: Dataset Preview ---
    with st.expander("📋 Dataset Preview (First 10 Rows)", expanded=True):
        st.dataframe(df.head(10), width="stretch")

    # --- EXPANDER 2: Descriptive Statistics ---
    with st.expander("📈 Descriptive Statistics"):
        # .astype(str) avoids a pyarrow serialization error: describe() mixes
        # datetime (from 'dob') and numeric stats in the same column.
        st.dataframe(df.describe(include="all").transpose().astype(str), width="stretch")

    # --- EXPANDER 3: Dataset Information ---
    with st.expander("ℹ️ Dataset Info"):
        st.write(f"**Rows:** {df.shape[0]}")
        st.write(f"**Columns:** {df.shape[1]}")
        st.write("**Column names (first 15):**")
        st.write(df.columns.tolist()[:15])

    # --- EXPANDER 4: Dataset Dictionary (HTML) ---
    with st.expander("📖 Dataset Dictionary (from Kaggle)"):
        show_html_description("./assets/dataset_description.html")


def show_html_description(html_path: str):
    """Render dataset description HTML if available."""
    html_file = Path(html_path)
    if html_file.exists():
        components.html(html_file.read_text(), height=400, scrolling=True)
    else:
        st.warning("⚠️ Dataset description file not found (`dataset_description.html`).")

