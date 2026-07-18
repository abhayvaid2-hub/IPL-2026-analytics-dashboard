def bat():
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import streamlit as st 
    df = pd.read_csv("cleaned_ipl_2026_deliveries.csv")
        
    

    top_n = st.select_slider(
        "Select Top Players",
        options=[5, 10, 15, 20, 25, 30],
        value=10
    )
    
    top10 = (
    df.groupby('striker')["runs_of_bat"].sum().sort_values(ascending=False).head(10))
    
    
    top10 = (
    df.groupby("striker")["runs_of_bat"]
      .sum()
      .sort_values(ascending=False)
      .head(top_n)
      .reset_index()
    )
        # Plotly Horizontal Bar Chart
    fig = px.bar(
            top10,
            x="runs_of_bat",
            y="striker",
            orientation="h",
            text="runs_of_bat",
            color="runs_of_bat",
            color_continuous_scale="Agsunset",
            title=f"🏏 Top {top_n} Run Scorers in IPL 2026"
        )

        # Highest scorer at the top
    fig.update_yaxes(categoryorder="total ascending")

        # Layout
    fig.update_layout(
        xaxis_title="Total Runs",
        title=dict(
        x=0.5,
        xanchor="center",
        font=dict(size=22)
        ),

            yaxis_title="Batsman",
            title_x=0.5,
            height=600,
            template="plotly_dark",
            coloraxis_showscale=False
        )

        # Text on bars
    fig.update_traces(
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Total Runs: %{x}<extra></extra>"
        )

        # Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    #---------------------------------------------------------------------------------------------------
    top_sixes = (
    df[df["runs_of_bat"] == 6]
    .groupby("striker")["runs_of_bat"]
    .count()
    .sort_values(ascending=False)
    
    .head(top_n)
    .reset_index()
    )
    top_sixes = top_sixes.rename(
    columns={"runs_of_bat": "sixes"}
    )

    top_sixes
    fig = px.bar(
    top_sixes,
    x="sixes",
    y="striker",
    orientation="h",
    text="sixes",
    color="sixes",
    color_continuous_scale="YlOrRd",
    title=f"🏏 Top {top_n} Six Hitters in IPL 2026"
    )

    # Highest value at top
    fig.update_yaxes(categoryorder="total ascending")

    # Layout
    fig.update_layout(
        title = dict( x=0.5,
        xanchor="center",
        font=dict(size=22)),
        
        template="plotly_white",
        height=550,
        xaxis_title="sixes",
        yaxis_title="Batsman",
        coloraxis_showscale=False
    )

    # Text Position
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Sixes: %{x}<extra></extra>"
    )

    # Streamlit
    st.plotly_chart(fig, use_container_width=True)
        
        
    #------------------------------------------------------------------------------------------
    
    top_fours = (
    df[df["runs_of_bat"] == 4]
    .groupby("striker")["runs_of_bat"]
    .count()
    .sort_values(ascending=False)
    .head(top_n)
    .reset_index()
    )

    top_fours = top_fours.rename(columns={"runs_of_bat": "fours"})

    top_fours
    fig = px.bar(
    top_fours,
    x="fours",
    y="striker",
    orientation="h",
    text="fours",
    color="fours",
    color_continuous_scale="RdYlGn_r",
    title=f"🏏 Top {top_n} Four Hitters in IPL 2026"
    )

    # Highest value at top
    fig.update_yaxes(categoryorder="total ascending")

    # Layout
    fig.update_layout(
        title=dict( x=0.5,
        xanchor="center",
        font=dict(size=22)),
        template="plotly_dark",
        height=550,
        xaxis_title="Total Fours",
        yaxis_title="Batsman",
        coloraxis_showscale=False
    )

    # Values on bars
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Total Fours: %{x}<extra></extra>"
    )

    # Show in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    
    #------------------------------------------------------------------------------------------------------------
    
    balls_faced = (
    df.groupby("striker")
    .size()
    .reset_index(name="balls")
    )
    
    batsman_runs = (
    df.groupby("striker")["runs_of_bat"]
    .sum()
    .reset_index()
    )
    
    strike_rate = pd.merge(
    batsman_runs,
    balls_faced,
    on="striker"
    )
    strike_rate["strike_rate"] = (
    strike_rate["runs_of_bat"] / strike_rate["balls"]
    ) * 100
    
    strike_rate = strike_rate[strike_rate["balls"] >= 100]
    top_strike_rate = (
    strike_rate.sort_values(by="strike_rate", ascending=False)
    .head(top_n)
    )
    top_strike_rate["strike_rate"] = top_strike_rate["strike_rate"].round(2)
    
  

    fig = px.bar(
        top_strike_rate,
        x="strike_rate",
        y="striker",
        orientation="h",
        text="strike_rate",
        color="strike_rate",
        color_continuous_scale="inferno_r",
        title=f"🏏 Top {top_n} Highest Strike Rate (Min. 100 Balls)"
    )

    # Highest Strike Rate at Top
    fig.update_yaxes(categoryorder="total ascending")

    # Layout
    fig.update_layout(
        title=dict( x=0.5,
        xanchor="center",
        font=dict(size=22)),
        template="plotly_dark",
        height=550,
        xaxis_title="Strike Rate",
        yaxis_title="Batsman",
        coloraxis_showscale=False
    )

    # Show values with 2 decimal places
    fig.update_traces(
        texttemplate="%{x:.2f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Strike Rate: %{x:.2f}<extra></extra>"
    )

    # Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    
    
    
    #------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    
    # Top 10 Run Scorers
    top10_runs = (
        df.groupby("striker")["runs_of_bat"]
        .sum()
        .sort_values(ascending=False)
    )

    top10_batsmen = top10_runs.head(top_n).index.tolist()

    # Heatmap Data
    heatmap_data = (
        df[df["striker"].isin(top10_batsmen)]
        .groupby(["striker", "runs_of_bat"])
        .size()
        .unstack(fill_value=0)
    )

    # Ensure all scoring shots exist
    for shot in [1, 2, 3, 4, 6]:
        if shot not in heatmap_data.columns:
            heatmap_data[shot] = 0

    # Keep only required columns
    heatmap_data = heatmap_data[[1, 2, 3, 4, 6]]

    # Rename columns
    heatmap_data.columns = [
        "Singles",
        "Doubles",
        "Triples",
        "Fours",
        "Sixes"
    ]

    # Arrange rows according to Top Run Scorers
    heatmap_data = heatmap_data.reindex(top10_batsmen)

    # Plotly Heatmap
    fig = px.imshow(
        heatmap_data,
        text_auto=True,
        color_continuous_scale="YlOrRd",
        aspect="auto",
        labels=dict(
            x="Scoring Shot",
            y="Batsman",
            color="Number of Scoring Shots"
        ),
        title=f"Scoring Pattern of Top {top_n} Run Scorers"
    )

    fig.update_layout(
        title=dict( x=0.5,
        xanchor="center",
        font=dict(size=22)),
        template="plotly_dark",
        height=650,
        xaxis_title="Scoring Shot",
        
        yaxis_title="Batsman"
    )

    # Streamlit
    st.plotly_chart(fig, use_container_width=True)

    #_________________________________________________________________________________________________________
     
    
    boundary_runs = {
    "Singles": (df["runs_of_bat"] == 1).sum() * 1,
    "Doubles": (df["runs_of_bat"] == 2).sum() * 2,
    "Triples": (df["runs_of_bat"] == 3).sum() * 3,
    "Fours": (df["runs_of_bat"] == 4).sum() * 4,
    "Sixes": (df["runs_of_bat"] == 6).sum() * 6,
    }
    

    # Data
    labels = ["Singles", "Doubles", "Triples", "Fours", "Sixes"]

    values = [
        (df["runs_of_bat"] == 1).sum() * 1,
        (df["runs_of_bat"] == 2).sum() * 2,
        (df["runs_of_bat"] == 3).sum() * 3,
        (df["runs_of_bat"] == 4).sum() * 4,
        (df["runs_of_bat"] == 6).sum() * 6
    ]

    # Total Runs
    total_runs = int(df["runs_of_bat"].sum())

    # Donut Chart
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            textinfo="label+percent",
            textfont_size=15,
            marker=dict(
                colors=[
                    "#2ECC71",   # Singles - Green
                    "#3498DB",   # Doubles - Blue
                    "#9B59B6",   # Triples - Purple
                    "#F39C12",   # Fours - Orange
                    "#E74C3C"    # Sixes - Red
                ],
                line=dict(color="white", width=3)
            ),
            hovertemplate="<b>%{label}</b><br>Runs: %{value:,}<br>Percentage: %{percent}<extra></extra>"
        )
    )

    # Layout
    fig.update_layout(
        title={
            "text": "<b>Runs Contribution by Scoring Shot</b>",
            "x": 0.5,
            "xanchor": "center",
            "font": dict(size=22)
        },
        annotations=[
            dict(
                text=f"<b>{total_runs:,}</b><br>Total Runs",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=22, color="#2c3e50")
            )
        ],
        showlegend=False,
        width=900,
        height=400,
        margin=dict(t=80, b=20, l=20, r=20)
    )
    st.plotly_chart(fig, use_container_width=True)