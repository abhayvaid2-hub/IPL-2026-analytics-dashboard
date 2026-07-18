def app():
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import streamlit as st 
    df = pd.read_csv("cleaned_ipl_2026_deliveries.csv")

    st.title("🏏 IPL 2026 Ball-by-Ball Analytics Dashboard")
    st.divider()
    st.caption("Analyze IPL 2026 ball-by-ball data with interactive visualizations and detailed performance insights.")
    st.divider()

    #----------------------------------------------------------------------------------------------------------------------------------------
    st.subheader("📋 Dashboard Overview")

    # ==========================
    # KPI CARD CSS
    # ==========================
    st.markdown("""
    <style>

    .kpi-card{
        background: linear-gradient(135deg,#1e293b,#334155);
        padding:20px;
        border-radius:15px;
        text-align:center;
        color:white;
        box-shadow:0px 4px 12px rgba(0,0,0,0.25);
        border:1px solid #475569;

        transition: all 0.3s ease;
        cursor:pointer;
    }

    .kpi-card:hover{
        transform: translateY(-8px);
        box-shadow: 0px 12px 25px rgba(0,0,0,0.45);
        border:1px solid #38bdf8;
    }

    .kpi-title{
        font-size:18px;
        color:#cbd5e1;
        font-weight:500;
    }

    .kpi-value{
        font-size:34px;
        font-weight:bold;
        color:#38bdf8;
        margin-top:8px;
    }

    </style>
    """, unsafe_allow_html=True)

    # ==========================
    # KPI VALUES
    # ==========================

    total_matches = df["match_no"].nunique()      # 74
    total_teams = df["batting_team"].nunique()    # 10
    total_players = df["striker"].nunique()       # 176
    total_venues = df["venue"].nunique()          # 13

    total_runs = int(df["total_runs"].sum())
    total_wickets = df["wicket_type"].notna().sum()
    total_fours = (df["runs_of_bat"] == 4).sum()
    total_sixes = (df["runs_of_bat"] == 6).sum()

    # ==========================
    # FIRST ROW
    # ==========================

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🏏 Total Matches</div>
            <div class="kpi-value">{total_matches}</div>
        </div>
        """,unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">👥 Teams</div>
            <div class="kpi-value">{total_teams}</div>
        </div>
        """,unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">⭐ Players</div>
            <div class="kpi-value">{total_players}</div>
        </div>
        """,unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🏟️ Venues</div>
            <div class="kpi-value">{total_venues}</div>
        </div>
        """,unsafe_allow_html=True)

    st.write("")

    # ==========================
    # SECOND ROW
    # ==========================

    col5,col6,col7,col8 = st.columns(4)

    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📈 Total Runs</div>
            <div class="kpi-value">{total_runs}</div>
        </div>
        """,unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🎯 Wickets</div>
            <div class="kpi-value">{total_wickets}</div>
        </div>
        """,unsafe_allow_html=True)

    with col7:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">💥 Fours</div>
            <div class="kpi-value">{total_fours}</div>
        </div>
        """,unsafe_allow_html=True)

    with col8:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🚀 Sixes</div>
            <div class="kpi-value">{total_sixes}</div>
        </div>
        """,unsafe_allow_html=True)
        
    #__________________________________________________________________________________________________________________-
    
    
    
    # =====================================================================
    # CLEANED DATASET
    # =====================================================================

        # st.divider()

        # st.subheader("📄 Cleaned IPL 2026 Dataset")

        # st.caption(
        #     "This dataset has been cleaned by removing duplicate records, handling missing values, standardizing data formats, and preparing it for analysis."
        # )

        # # Dataset Summary
        # col1, col2, col3, col4 = st.columns(4)

        # with col1:
        #     st.metric("Rows", df.shape[0])

        # with col2:
        #     st.metric("Columns", df.shape[1])

        # with col3:
        #     st.metric("Missing Values", df.isnull().sum().sum())

        # with col4:
        #     st.metric("Duplicate Rows", df.duplicated().sum())

        # st.write("")

        # # Full Cleaned Dataset
        # st.dataframe(
        #     df,
        #     use_container_width=True,
        #     hide_index=True
        # )

        # # Download Button
        # csv = df.to_csv(index=False)

        # st.download_button(
        #     label="📥 Download Cleaned Dataset",
        #     data=csv,
        #     file_name="cleaned_ipl_2026_deliveries.csv",
        #     mime="text/csv"
        # )
        
    #_________________________________________________________________________________________________________________
    # =====================================================================
    # 📄 CLEANED DATASET SECTION
    # =====================================================================


    st.divider()

    st.subheader("📄 Cleaned IPL 2026 Dataset")

    st.caption(
        "This dataset has been cleaned by removing duplicate records, standardizing data formats, creating new analytical features, and preparing it for interactive visualization."
    )

    # ---------------------------------------------------------------------
    # Dataset Summary
    # ---------------------------------------------------------------------

    duration = (
    pd.to_datetime(df["date"]).max()
    - pd.to_datetime(df["date"]).min()
    ).days + 1
    col1, col2, col3, col4 = st.columns(4)
    

    with col1:
        st.metric("📄 Total Records", f"{df.shape[0]:,}")

    with col2:
        st.metric("📑 Columns", df.shape[1])

    with col3:
         st.metric("🗓️ Tournament Duration", f"{duration} Days")

    with col4:
         st.metric("🏟️ Venues Covered", df["venue"].nunique())

    st.write("")

    # ---------------------------------------------------------------------
    # Data Cleaning Summary
    # ---------------------------------------------------------------------

    with st.expander("🧹 Data Cleaning Summary", expanded=False):

        st.markdown("""
    ### ✅ Data Cleaning Steps Performed

    - ✔ Removed duplicate records
    - ✔ Standardized player names
    - ✔ Standardized team names
    - ✔ Corrected inconsistent data formats
    - ✔ Created **Total Runs** feature
    - ✔ Created **Match Phase** feature (Powerplay, Middle Overs, Death Overs)
    - ✔ Verified dataset integrity
    - ✔ Prepared dataset for visualization and dashboard development
    """)

    st.write("")

    # ---------------------------------------------------------------------
    # Remove Unnamed Column (if exists)
    # ---------------------------------------------------------------------

    display_df = df.copy()

    if "Unnamed: 0" in display_df.columns:
        display_df = display_df.drop(columns=["Unnamed: 0"])

    # ---------------------------------------------------------------------
    # Dataset Preview
    # ---------------------------------------------------------------------

    st.subheader("📋 Cleaned Dataset Preview")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # ---------------------------------------------------------------------
    # Download Button
    # ---------------------------------------------------------------------

    st.write("")

    csv = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Cleaned Dataset",
        data=csv,
        file_name="cleaned_ipl_2026_deliveries.csv",
        mime="text/csv"
    )