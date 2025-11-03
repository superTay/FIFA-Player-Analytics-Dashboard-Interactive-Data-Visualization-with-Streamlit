"""
Page 1: Introduction and dataset loading.

This module handles:
- Basic app introduction and dataset source.
- Downloading the FIFA dataset from URL.
- Caching and storing the dataframe in Streamlit session state.
"""

import streamlit as st
import pandas as pd


def show():
    """Render the Introduction page with dataset loading and summary."""

    # --- PAGE HEADER ---
    st.title("🏁 FIFA Player Analytics Dashboard ⚽")
    st.write("""
    This project analyzes FIFA player statistics, allowing users to explore,
    filter, and visualize data related to player performance and attributes.
    """)

    # --- DATASET URL ---
    DATA_URL = (
        "https://raw.githubusercontent.com/stefanoleone992/"
        "FIFA-21-complete-player-dataset/main/players_21.csv"
    )

    st.markdown(f"📂 **Data source:** [Kaggle - FIFA 21 Dataset]({DATA_URL})")

    # --- DATA LOADING FUNCTION ---
    @st.cache_data
    def get_data(url: str) -> pd.DataFrame:
        """
        Download and load the FIFA dataset from the given URL.

        Parameters
        ----------
        url : str
            URL pointing to the CSV dataset.

        Returns
        -------
        pd.DataFrame
            Loaded FIFA player data.
        """
        df = pd.read_csv(url)
        return df