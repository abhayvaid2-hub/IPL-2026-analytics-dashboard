def venue():
    import pandas as pd
    import plotly.express as px
    import matplotlib.pyplot as plt
    import seaborn as sns
    import streamlit as st 
    import plotly.graph_objects as go
    df = pd.read_csv("cleaned_ipl_2026_deliveries.csv")
    
    innings_score = (
    df.groupby(["match_no", "innings", "batting_team"], as_index=False)
    .agg(
    Runs=("total_runs", "sum"),
    Wickets=("player_dismissed", lambda x: x.notna().sum())
    )
    )
    venue_scores = (
    df.groupby(["venue", "innings"])["total_runs"]
      .sum()
      .reset_index()
    )
    
    #____________________________________------------------------------------------------------------------------_______________---
    # Count total matches hosted by each venue
    venue_matches = (
        df.groupby("venue")["match_no"]
        .nunique()
        .reset_index(name="Matches Hosted")
        .sort_values("Matches Hosted", ascending=True)
    )

    fig = px.bar(
        venue_matches,
        x="Matches Hosted",
        y="venue",
        orientation="h",
        text="Matches Hosted",
        color="Matches Hosted",
        color_continuous_scale="Blues",
        title="🏟️ Total Matches Hosted by Each Venue"
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Matches Hosted: %{x}<extra></extra>"
    )

    fig.update_layout(
         title={
        "text": "🏟️ Total Matches Hosted by Each Venue",
        "x": 0.5,
        "xanchor": "center",
        "font": dict(size=22)
    },
        template="plotly_white",
        height=600,
        xaxis_title="Number of Matches",
        yaxis_title="",
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    #________________________________________________________________________________________________________

    venue_phase = (
    df.groupby(["venue", "phase"])["total_runs"]
      .sum()
      .reset_index()
    )

    phase_order = [
        "Powerplay",
        "Middle Overs",
        "Death Overs"
    ]

    fig = px.area(
        venue_phase,
        x="venue",
        y="total_runs",
        color="phase",
        category_orders={"phase": phase_order},
        color_discrete_map={
            "Powerplay":"#00CC96",
            "Middle Overs":"#FFA15A",
            "Death Overs":"#EF553B"
        },
        markers=True,
        title="Venue Scoring Pattern Across Match Phases"
    )

    fig.update_layout(
        title={
        "text": "Venue Scoring Pattern Across Match Phases",
        "x": 0.5,
        "xanchor": "center",
        "font": dict(size=22)
        },
        template="plotly_white",
        xaxis_tickangle=-35,
        height=650,
        legend_title=""
    )

    st.plotly_chart(fig, use_container_width=True)
    
    
    #----------------------------------------------------------------------------------------------------------------------
    
        # Total score of every innings
    innings_score = (
        df.groupby(["match_no", "venue", "innings"])["total_runs"]
        .sum()
        .reset_index(name="Innings Score")
    )

    # Average innings score at each venue
    venue_avg = (
        innings_score.groupby("venue")["Innings Score"]
        .mean()
        .reset_index(name="Average Score")
        .sort_values("Average Score", ascending=True)
    )

    fig = px.bar(
        venue_avg,
        x="Average Score",
        y="venue",
        orientation="h",
        text="Average Score",
        color="Average Score",
        color_continuous_scale="YlOrRd",
        title="🏟️ Average Innings Score by Venue"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Average Score : %{x:.1f}<extra></extra>"
    )

    fig.update_layout(
        template="plotly_white",
        height=600,
        title={
        "text": "🏟️ Average Innings Score by Venue",
        "x": 0.5,
        "xanchor": "center",
        "font": dict(size=22)
        },
        
        xaxis_title="Average Innings Score",
        yaxis_title="",
        coloraxis_showscale=False,
        font=dict(size=14),
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)
    
    #_________________________________________________________________________________________________________________------
    
    # Boundary Percentage Calculation
    venue_boundary = (
        df.groupby("venue")
        .agg(
            Total_Balls=("runs_of_bat", "count"),
            Boundaries=("runs_of_bat", lambda x: ((x == 4) | (x == 6)).sum())
        )
        .reset_index()
    )

    venue_boundary["Boundary %"] = (
        venue_boundary["Boundaries"] / venue_boundary["Total_Balls"] * 100
    ).round(2)

    venue_boundary = venue_boundary.sort_values("Boundary %", ascending=True)

    # Figure
    fig = go.Figure()

    # Lollipop Line
    fig.add_trace(go.Scatter(
        x=venue_boundary["Boundary %"],
        y=venue_boundary["venue"],
        mode="lines",
        line=dict(color="#A9A9A9", width=3),
        hoverinfo="skip",
        showlegend=False
    ))

    # Lollipop Dots
    fig.add_trace(go.Scatter(
        x=venue_boundary["Boundary %"],
        y=venue_boundary["venue"],
        mode="markers+text",
        marker=dict(
            size=14,
            color=venue_boundary["Boundary %"],
            colorscale="Turbo",
            line=dict(color="white", width=2),
            showscale=False
        ),
        text=venue_boundary["Boundary %"].astype(str) + "%",
        textposition="middle right",
        hovertemplate="<b>%{y}</b><br>Boundary % : %{x:.2f}%<extra></extra>",
        showlegend=False
    ))

    fig.update_layout(
         title={
        "text": "🏟️ Boundary Percentage by Venue",
        "x": 0.5,
        "xanchor": "center",
        "font": dict(size=22)
        },
        template="plotly_white",
        height=600,
        title_x=0.5,
        xaxis_title="Boundary Percentage (%)",
        yaxis_title="",
        font=dict(size=14),
        margin=dict(l=20, r=40, t=60, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)