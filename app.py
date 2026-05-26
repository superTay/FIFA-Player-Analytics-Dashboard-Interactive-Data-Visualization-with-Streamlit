"""
Main Streamlit app for FIFA Player Analytics Dashboard.

This script defines the overall structure, configuration, and navigation
between pages (Intro, Data Visualization, and Predictive Model).

Author: Christian Marzal Della Rovere
"""

import streamlit as st
from modules import page_intro, page_data_viz, page_model_inference



def main():
    """Main function to configure the Streamlit app and handle page navigation."""

    # --- APP CONFIGURATION ---
    st.set_page_config(
        page_title="FIFA Player Analytics ⚽",
        page_icon="⚽",
        layout="wide",
        menu_items={
            'Get help': 'https://docs.streamlit.io/',
            'Report a bug': 'https://github.com/superTay/FIFA-Player-Analytics-Dashboard-Interactive-Data-Visualization-with-Streamlit',
            'About': 'Developed by Christian Marzal Della Rovere as a Streamlit Advanced Module project.'
        }
    )

 # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        ("🏁 Introduction", "📈 Data Visualization", "🤖 Predictive Model")
    )

    # --- PAGE ROUTING ---
    if page == "🏁 Introduction":
        page_intro.show()
    elif page == "📈 Data Visualization":
        page_data_viz.show()
    elif page == "🤖 Predictive Model":
        page_model_inference.show()


if __name__ == "__main__":
    main()