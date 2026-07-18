def bowl():
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
    
    
    pd.DataFrame(
    sorted(df["bowler"].unique()),
    columns=["Bowler"]
    )
    valid_wickets = df[
    ~df["wicket_type"].isin([
        "runout",
        "retired hurt",
        "obstructing the field"
    ])
    ]
    valid_wickets = valid_wickets.dropna(subset=["wicket_type"])
    top_wickets = valid_wickets.groupby('bowler')['wicket_type'].count().sort_values(ascending=False).head(top_n).reset_index()
    top_wickets = top_wickets.rename(
    columns={"wicket_type": "wickets"}
    )
    fig = px.bar(
    top_wickets,
    x="wickets",
    y="bowler",
    orientation="h",
    text="wickets",
    color="wickets",
    color_continuous_scale="magma",
    title=f"🏏 Top{top_n} Wicket Takers in IPL 2026"
    )
    

    # Highest wicket taker at top
    fig.update_yaxes(categoryorder="total ascending")

    # Layout
    # fig.update_layout(
    #     title_x=0.5,
    #     template="plotly_dark",
    #     height=550,
    #     xaxis_title="Total Wickets",
    #     yaxis_title="Bowler",
    #     coloraxis_showscale=False,
        
    # )
    fig.update_layout(
    title=dict(
        text= f"🏏 Top {top_n} Wicket Takers in IPL 2026",
        x=0.5,
        xanchor="center",
        font=dict(size=22)
    ),
    template="plotly_dark",
    height=550,
    xaxis_title="Total Wickets",
    yaxis_title="Bowler",
    coloraxis_showscale=False
    )
    

    # Values on bars
    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Total Wickets: %{x}<extra></extra>"
    )

    # Streamlit
    st.plotly_chart(fig, use_container_width=True)
    #------------------------------------------------------------------------------------------------------------------------------
    
    df["wide"].value_counts().sort_index()
    df["noballs"].value_counts().sort_index()
    df["extras"].value_counts().sort_index()
    df["wicket_type"].value_counts(dropna=False)
    df.groupby("bowler").size().sort_values(ascending=False).head(top_n)
    economy = df.copy()

    # Runs conceded
    economy["runs_conceded"] = (
        economy["runs_of_bat"] +
        economy["wide"] +
        economy["noballs"]
    )

    # Bowling statistics
    bowling_stats = economy.groupby("bowler").agg(
        runs_conceded=("runs_conceded", "sum"),
        legal_balls=("wide", lambda x: (
            (economy.loc[x.index, "wide"] == 0) &
            (economy.loc[x.index, "noballs"] == 0)
        ).sum())
    ).reset_index()

    # Overs Bowled
    bowling_stats["overs"] = bowling_stats["legal_balls"] / 6

    # Economy Rate
    bowling_stats["economy"] = (
        bowling_stats["runs_conceded"] /
        bowling_stats["overs"]
    )

    # Minimum Qualification (20 Overs)
    qualified = bowling_stats[
        bowling_stats["legal_balls"] >= 120
    ]

    # Top 10 Economy Bowlers
    top10 = qualified.sort_values(
        by="economy",
        ascending=True
    ).head(10)

    # -----------------------------
    # Plotly Chart
    # -----------------------------

    fig = px.bar(
        top10,
        x="economy",
        y="bowler",
        orientation="h",
        text="economy",
        color="economy",
        color_continuous_scale="tealgrn",
        title=f"🎯 Top {top_n} Economy Bowlers (Minimum 20 Overs)"
    )

    # Lowest Economy at Top
    fig.update_yaxes(categoryorder="total descending")

    # Layout
    fig.update_layout(
        title=dict(x=0.5,
        xanchor="center",
        font=dict(size=22)),
        template="plotly_dark",
        height=550,
        xaxis_title="Economy Rate",
        yaxis_title="Bowler",
        coloraxis_showscale=False
    )

    # Value Labels & Hover
    fig.update_traces(
        texttemplate="%{x:.2f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Economy Rate: %{x:.2f}<extra></extra>"
    )

    # Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    #--------------------------------------------------------------------------------------------------------------------------

    # --------------------------------------------------
    # Calculate Bowling Strike Rate
    # --------------------------------------------------

    bowling_df = df.copy()

    # Valid wickets only (exclude run out & retired hurt)
    valid_wickets = [
        "bowled",
        "caught",
        "lbw",
        "stumped",
        "hit wicket"
    ]

    # Runs conceded
    bowling_df["runs_conceded"] = (
        bowling_df["runs_of_bat"] +
        bowling_df["wide"] +
        bowling_df["noballs"]
    )

    # Legal delivery
    bowling_df["legal_ball"] = (
        (bowling_df["wide"] == 0) &
        (bowling_df["noballs"] == 0)
    ).astype(int)

    # Wicket credited to bowler
    bowling_df["bowler_wicket"] = (
        bowling_df["wicket_type"].isin(valid_wickets)
    ).astype(int)

    # Bowling statistics
    strike_rate = bowling_df.groupby("bowler").agg(
        legal_balls=("legal_ball", "sum"),
        wickets=("bowler_wicket", "sum")
    ).reset_index()

    # Remove bowlers with 0 wickets
    strike_rate = strike_rate[strike_rate["wickets"] > 0]

    # Minimum 20 Overs (120 legal balls)
    strike_rate = strike_rate[strike_rate["legal_balls"] >= 120]

    # Bowling Strike Rate
    strike_rate["bowling_sr"] = (
        strike_rate["legal_balls"] /
        strike_rate["wickets"]
    )

    # Top 10 (Lowest Strike Rate is Best)
    top10_sr = strike_rate.sort_values(
        by="bowling_sr"
    ).head(top_n)


    # --------------------------------------------------
    # Plotly Chart
    # --------------------------------------------------

    fig = px.bar(
        top10_sr,
        x="bowling_sr",
        y="bowler",
        orientation="h",
        text="bowling_sr",
        color="bowling_sr",
        color_continuous_scale="magma",
        title="🎯 Best Bowling Strike Rate (Minimum 20 Overs)"
    )

    # Lowest Strike Rate at Top
    fig.update_yaxes(categoryorder="total descending")

    # Layout
    fig.update_layout(
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=22)
        ),
        template="plotly_dark",
        height=550,
        xaxis_title="Balls Per Wicket",
        yaxis_title="Bowler",
        coloraxis_showscale=False
    )

    # Value Labels
    fig.update_traces(
        texttemplate="%{x:.1f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Bowling Strike Rate: %{x:.1f}<extra></extra>"
    )

    # Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    
    #----------------------------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------------------------------------- 
    # -----------------------------------------
    # Dot Ball Specialists
    # -----------------------------------------

    dot_df = df.copy()

    # Legal dot ball
    dot_df["dot_ball"] = (
        (dot_df["runs_of_bat"] == 0) &
        (dot_df["wide"] == 0) &
        (dot_df["noballs"] == 0)
    ).astype(int)

    # Legal delivery
    dot_df["legal_ball"] = (
        (dot_df["wide"] == 0) &
        (dot_df["noballs"] == 0)
    ).astype(int)

    # Bowling Summary
    dot_stats = dot_df.groupby("bowler").agg(
        dot_balls=("dot_ball", "sum"),
        legal_balls=("legal_ball", "sum")
    ).reset_index()

    # Overs
    dot_stats["overs"] = dot_stats["legal_balls"] / 6

    # Minimum Qualification (20 Overs)
    dot_stats = dot_stats[
        dot_stats["legal_balls"] >= 120
    ]

    # Top 10
    top10_dot = dot_stats.sort_values(
        by="dot_balls",
        ascending=False
    ).head(top_n)

    # -----------------------------------------
    # Plotly Chart
    # -----------------------------------------

    fig = px.bar(
        top10_dot,
        x="dot_balls",
        y="bowler",
        orientation="h",
        text="dot_balls",
        color="dot_balls",
        color_continuous_scale="tealgrn",
        title=f"🎯 Top {top_n} Dot Ball Specialists (Minimum 20 Overs)"
    )

    # Highest Dot Balls at Top
    fig.update_yaxes(categoryorder="total ascending")

    # Layout
    fig.update_layout(
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(size=22)
        ),
        template="plotly_dark",
        height=550,
        xaxis_title="Dot Balls Bowled",
        yaxis_title="Bowler",
        coloraxis_showscale=False
    )

    # Value Labels & Hover
    fig.update_traces(
        texttemplate="%{x}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Dot Balls: %{x}<extra></extra>"
    )

    # Streamlit
    st.plotly_chart(fig, use_container_width=True)


#________________________________________________________________________________________________________________________

 # -----------------------------
    # Valid Wickets
    # -----------------------------

    valid_dismissals = df[df["wicket_type"].notna()].copy()

    def group_wicket_type(wt):
        mapping = {
            "caught": "Caught",
            "bowled": "Bowled",
            "lbw": "LBW",
            "runout": "Run Out",
            "stumped": "Stumped",
            "hit wicket": "Hit Wicket"
        }
        return mapping.get(wt, "Others")

    valid_dismissals["wicket_group"] = valid_dismissals["wicket_type"].apply(group_wicket_type)

    wicket_dist = valid_dismissals["wicket_group"].value_counts()

    order = [
        "Caught",
        "Bowled",
        "Run Out",
        "LBW",
        "Stumped",
        "Hit Wicket",
        "Others"
    ]

    wicket_dist = wicket_dist.reindex(order).dropna()

    # Premium Colors
    colors = [
        "#233B8B",   # Caught
        "#3F73A8",   # Bowled
        "#F59E0B",   # Run Out
        "#4CAF6A",   # LBW
        "#E53935",   # Stumped
        "#7E57C2",   # Hit Wicket
        "#6C757D"    # Others
    ]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=wicket_dist.index,
                values=wicket_dist.values,
                hole=0.55,
                textinfo="label+percent",
                textfont_size=13,
                marker=dict(
                    colors=colors,
                    line=dict(color="white", width=3)
                ),
                sort=False,
                hovertemplate="<b>%{label}</b><br>Wickets: %{value}<br>Percentage: %{percent}<extra></extra>"
            )
        ]
    )

    fig.update_layout(

        title=dict(
            text="<b>Wicket Type Distribution — IPL 2026</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=22)
        ),

        annotations=[
            dict(
                text=f"<b>{int(wicket_dist.sum())}</b><br>Total Wickets",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=22)
            )
        ],

        legend=dict(
            orientation="v",
            y=0.95,
            x=1.02
        ),

        template="plotly_dark",

        height=400,

        margin=dict(
            t=80,
            b=40,
            l=40,
            r=120
        )

    )

    # Streamlit
    st.plotly_chart(fig, use_container_width=True)


