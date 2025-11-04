# modules/page_data_viz.py
"""
Page 2: Data Visualization — Step 2
Adds cached unique-value extraction and advanced filter widgets.
"""

import streamlit as st
import pandas as pd


def show():
    """Render the Data Visualization page (Step 2: advanced filters)."""

    st.header("📊 Player Data Exploration and Visualization")

    # --- VERIFY SESSION STATE ---
    if "df" not in st.session_state or st.session_state["df"].empty:
        st.warning("⚠️ No data loaded. Please start from the Introduction page.")
        return

    df = st.session_state["df"]

    # --- HELPER FUNCTION TO GET UNIQUE VALUES (CACHED) ---
    @st.cache_data
    def get_values(column: str):
        """Return sorted unique values from a given DataFrame column (cached)."""
        return sorted(df[column].dropna().unique().tolist())

    # --- FILTERS EXPANDER ---
    with st.expander("🎛️ Data Filters", expanded=True):

        with st.form("filter_form"):
            st.write("Select filters below to refine the dataset for visualization.")

            # --- TWO-COLUMN LAYOUT ---
            col1, col2 = st.columns(2)

            # 🟢 CATEGORICAL FILTERS (LEFT)
            with col1:
                selected_nationalities = st.multiselect(
                    "Nationality",
                    options=get_values("nationality"),
                    default=[],
                )

                selected_clubs = st.multiselect(
                    "Club Name",
                    options=get_values("club_name"),
                    default=[],
                )

                selected_positions = st.multiselect(
                    "Player Position(s)",
                    options=get_values("player_positions"),
                    default=[],
                )

                selected_foot = st.multiselect(
                    "Preferred Foot",
                    options=get_values("preferred_foot"),
                    default=[],
                )

            # 🔵 NUMERIC FILTERS (RIGHT)
            with col2:
                age_min, age_max = st.slider(
                    "Age Range",
                    min_value=int(df["age"].min()),
                    max_value=int(df["age"].max()),
                    value=(18, 35),
                )

                overall_min, overall_max = st.slider(
                    "Overall Rating Range",
                    min_value=int(df["overall"].min()),
                    max_value=int(df["overall"].max()),
                    value=(70, 90),
                )

                potential_min, potential_max = st.slider(
                    "Potential Range",
                    min_value=int(df["potential"].min()),
                    max_value=int(df["potential"].max()),
                    value=(70, 90),
                )

                value_min, value_max = st.slider(
                    "Market Value (€)",
                    min_value=int(df["value_eur"].min()),
                    max_value=int(df["value_eur"].max()),
                    value=(
                        int(df["value_eur"].quantile(0.25)),
                        int(df["value_eur"].quantile(0.75)),
                    ),
                )

            # --- FORM SUBMIT BUTTON ---
            submit_button = st.form_submit_button("✅ Update DataFrame")

    # --- APPLY FILTERS ON SUBMIT ---
    if submit_button:
        df_filtered = df.copy()

        # Apply categorical filters
        if selected_nationalities:
            df_filtered = df_filtered[df_filtered["nationality"].isin(selected_nationalities)]

        if selected_clubs:
            df_filtered = df_filtered[df_filtered["club_name"].isin(selected_clubs)]

        if selected_positions:
            df_filtered = df_filtered[
                df_filtered["player_positions"].isin(selected_positions)
            ]

        if selected_foot:
            df_filtered = df_filtered[df_filtered["preferred_foot"].isin(selected_foot)]

        # Apply numeric filters
        df_filtered = df_filtered[
            (df_filtered["age"].between(age_min, age_max))
            & (df_filtered["overall"].between(overall_min, overall_max))
            & (df_filtered["potential"].between(potential_min, potential_max))
            & (df_filtered["value_eur"].between(value_min, value_max))
        ]

        # Store filtered data for next visualization step
        st.session_state["df_filtered"] = df_filtered

        # Display summary
        st.success(f"✅ {len(df_filtered):,} players match the selected filters.")
        st.dataframe(df_filtered.head(10), use_container_width=True)

    else:
        st.info("Adjust filters and click **Update DataFrame** to apply changes.")

