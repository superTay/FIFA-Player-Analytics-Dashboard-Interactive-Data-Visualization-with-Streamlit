# modules/page_data_viz.py
"""
Page 2: Data Visualization — Steps 3 & 4
Adds filtering logic and interactive Plotly charts.
"""

import streamlit as st
import pandas as pd
import plotly.express as px


def show():
    """Render the Data Visualization page with filters and interactive charts."""

    st.header("📊 Player Data Exploration and Visualization")

    # --- VERIFY SESSION STATE ---
    if "df" not in st.session_state or st.session_state["df"].empty:
        st.warning("⚠️ No data loaded. Please start from the Introduction page.")
        return

    df = st.session_state["df"]

    # --- HELPER FUNCTION TO CACHE UNIQUE VALUES ---
    @st.cache_data
    def get_values(column: str):
        """Return sorted unique values from a given column."""
        return sorted(df[column].dropna().unique().tolist())

    # --- DATAFRAME UPDATE FUNCTION ---
    def update_df(
        nationalities, clubs, positions, foot, 
        age_range, overall_range, potential_range, value_range
    ):
        """Apply all filters and return filtered DataFrame."""
        df_filtered = df.copy()

        # Apply categorical filters
        if nationalities:
            df_filtered = df_filtered[df_filtered["nationality"].isin(nationalities)]
        if clubs:
            df_filtered = df_filtered[df_filtered["club_name"].isin(clubs)]
        if positions:
            df_filtered = df_filtered[df_filtered["player_positions"].isin(positions)]
        if foot:
            df_filtered = df_filtered[df_filtered["preferred_foot"].isin(foot)]

        # Apply numeric filters
        df_filtered = df_filtered[
            (df_filtered["age"].between(age_range[0], age_range[1]))
            & (df_filtered["overall"].between(overall_range[0], overall_range[1]))
            & (df_filtered["potential"].between(potential_range[0], potential_range[1]))
            & (df_filtered["value_eur"].between(value_range[0], value_range[1]))
        ]

        st.session_state["df_fil"] = df_filtered
        return df_filtered

    # --- FILTERS ---
    with st.expander("🎛️ Data Filters", expanded=True):

        with st.form("filter_form"):
            col1, col2 = st.columns(2)

            # 🟢 LEFT: CATEGORICAL FILTERS
            with col1:
                nationalities = st.multiselect("Nationality", options=get_values("nationality"))
                clubs = st.multiselect("Club Name", options=get_values("club_name"))
                positions = st.multiselect("Player Position(s)", options=get_values("player_positions"))
                foot = st.multiselect("Preferred Foot", options=get_values("preferred_foot"))

            # 🔵 RIGHT: NUMERIC FILTERS
            with col2:
                age_range = st.slider("Age Range", int(df["age"].min()), int(df["age"].max()), (18, 35))
                overall_range = st.slider("Overall Rating", int(df["overall"].min()), int(df["overall"].max()), (70, 90))
                potential_range = st.slider("Potential", int(df["potential"].min()), int(df["potential"].max()), (70, 90))
                value_range = st.slider("Market Value (€)", 
                    int(df["value_eur"].min()), int(df["value_eur"].max()),
                    (int(df["value_eur"].quantile(0.25)), int(df["value_eur"].quantile(0.75)))
                )

            # Submit button
            submitted = st.form_submit_button("✅ Update DataFrame")

    # --- APPLY FILTERS ---
    if submitted:
        df_fil = update_df(
            nationalities, clubs, positions, foot,
            age_range, overall_range, potential_range, value_range
        )

        st.success(f"✅ {len(df_fil):,} players match the filters.")
        st.dataframe(df_fil.head(10), use_container_width=True)
    else:
        st.info("Adjust filters and click **Update DataFrame** to refresh data.")

    # --- VISUALIZATION SECTION ---
    if "df_fil" in st.session_state and not st.session_state["df_fil"].empty:
        df_fil = st.session_state["df_fil"]

        st.markdown("---")
        st.subheader("📈 Interactive Data Visualization")

        col_plot1, col_plot2 = st.columns([5, 1])
        fig_container = col_plot1.empty()  # container for dynamic plot

        # 🎨 PLOT CONFIGURATION PANEL
        with col_plot2:
            plot_type = st.selectbox(
                "Plot Type",
                options=["Scatter", "Histogram", "Box", "Bar"],
                index=0
            )
            x_col = st.selectbox("X-axis", options=df_fil.select_dtypes(include=["number", "category"]).columns)
            y_col = st.selectbox("Y-axis", options=df_fil.select_dtypes(include=["number"]).columns)
            color_col = st.selectbox("Color", options=["None"] + df_fil.select_dtypes(include=["object", "category"]).columns.tolist())

        # --- PLOT GENERATION ---
        def generate_plot(df: pd.DataFrame, plot_type: str, x: str, y: str, color: str):
            """Generate a Plotly figure based on user configuration."""
            color_arg = color if color != "None" else None

            if plot_type == "Scatter":
                fig = px.scatter(df, x=x, y=y, color=color_arg, trendline="ols", opacity=0.7)
            elif plot_type == "Histogram":
                fig = px.histogram(df, x=x, color=color_arg, nbins=30)
            elif plot_type == "Box":
                fig = px.box(df, x=x, y=y, color=color_arg)
            elif plot_type == "Bar":
                fig = px.bar(df, x=x, y=y, color=color_arg)
            else:
                fig = px.scatter(df, x=x, y=y)

            fig.update_layout(
                template="plotly_dark",
                height=500,
                margin=dict(l=20, r=20, t=40, b=40),
                title=dict(text=f"{plot_type} Plot of {y} vs {x}", x=0.5),
            )
            return fig

        # Render the selected plot
        fig = generate_plot(df_fil, plot_type, x_col, y_col, color_col)
        fig_container.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No filtered data available. Apply filters to generate a plot.")


