import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st 
from streamlit_option_menu import option_menu
import home
import batting
import bowling
import team_analy
import venue_analy


st.set_page_config(
    page_title="IPL 2026 Ball-by-Ball Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:

    selected = option_menu(
        menu_title="🏏 IPL\nDashboard",
        

        options=[
            "Home",
            "Batting Analysis",
            "Bowling Analysis",
            "Team Analysis",
            "Venue Analysis"
        ],

        icons=[
            "house-fill",
            "trophy-fill",
            "bullseye",
            "people-fill",
            "geo-alt-fill"
        ],

        menu_icon= "clipboard-data",
        default_index=0
    )
    styles={
            "container": {
                "padding": "12px",
                "background-color": "#111827",
                "border-radius": "15px",
            },
            "icon": {
                "color": "white",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "6px 0",
                "padding": "12px",
                "--hover-color": "#262730",
            },
            "nav-link-selected": {
                "background-color": "#FF4B4B",
            },
        }

    # ------------------------------------------
    # Built With
    # ------------------------------------------
    st.markdown(
    """
    <h4 style="text-align:center;">
        💻 Built With
    </h4>
    """,
    unsafe_allow_html=True
)

    st.markdown(    
    """
    <div style="
        text-align:center;
        line-height:2;
        font-size:15px;
    ">
        🐍 Python<br>
        ⚡ Streamlit<br>
        📊 Plotly<br>
        🐼 Pandas<br>
        📈 NumPy
        </div>
        """,
        unsafe_allow_html=True
    )
    # ------------------------------------------
    # Footer
    # ------------------------------------------

    st.markdown(
        """
        <div style='text-align:center;color:#9CA3AF;font-size:13px;line-height:1.6'>
            🏏 IPL 2026 Analytics Dashboard<br>
            <b>Version 1.0</b>
        </div>
        """,
        unsafe_allow_html=True
    )
    
if selected == "Home":
    home.app()

elif selected == "Batting Analysis":
    st.title("🏏 Batting Analysis")
    st.divider()
    st.write("Top Run Scorers, Strike Rate, Boundary Analysis, Scoring Patterns")
    st.divider()    
    
    batting.bat()

elif selected == "Bowling Analysis":
    st.title("🎯 Bowling Analysis")
    st.divider()
    st.write("Top Wicket Takers, Economy Rate, Bowling Stats")
    st.divider()
    bowling.bowl()

elif selected == "Team Analysis":
    st.title("👥 Team Analysis")
    st.divider()
    st.write("Team Performance and Comparison")
    st.divider()
    team_analy.team()

elif selected == "Venue Analysis":
    st.title("🏟️ Venue Analysis")
    st.divider()
    st.write("Venue Wise Analysis and Average Scores")
    st.divider()
    venue_analy.venue()
    
    
    

