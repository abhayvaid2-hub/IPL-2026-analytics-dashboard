def team():
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    import streamlit as st 
    df = pd.read_csv("cleaned_ipl_2026_deliveries.csv")
    df.groupby("batting_team")["runs_of_bat"].sum().sort_values(ascending=False)
    # ---------------------------------------------
    # Total Runs Per Innings
    # ---------------------------------------------

    df["total_runs"] = df["runs_of_bat"] + df["extras"]

    innings_total = (
        df.groupby(["match_no", "innings", "batting_team"], as_index=False)
        .agg(Total_Runs=("total_runs", "sum"))
    )

    # ---------------------------------------------
    # Average Team Score
    # ---------------------------------------------

    avg_score = (
        innings_total
        .groupby("batting_team", as_index=False)
        .agg(Average_Score=("Total_Runs", "mean"))
        .sort_values("Average_Score", ascending=False)
    )

    # ---------------------------------------------
    # Plotly Chart
    # ---------------------------------------------

    fig = px.bar(
        avg_score,
        x="Average_Score",
        y="batting_team",
        orientation="h",
        text="Average_Score",
        color="Average_Score",
        color_continuous_scale="Blues",
        title="🏏 Average Team Score Per Innings — IPL 2026"
    )

    # Highest Average Score at Top
    fig.update_yaxes(categoryorder="total ascending")

    # Layout
    fig.update_layout(
        title=dict(
            x=0.5,
            font=dict(size=22),
            xanchor="center"
        ),
        template="plotly_dark",
        height=550,
        xaxis_title="Average Runs",
        yaxis_title="Team",
        coloraxis_showscale=False
    )

    # Value Labels
    fig.update_traces(
        texttemplate="%{x:.1f}",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Average Score: %{x:.1f}<extra></extra>"
    )

    # Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    #------------------------------------------------------------------------------------------------------------------------
    # -------------------------------
    # Team Boundary Comparison
    # -------------------------------

    team_boundary = (
        df.groupby("batting_team")
        .agg(
            Fours=("runs_of_bat", lambda x: (x == 4).sum()),
            Sixes=("runs_of_bat", lambda x: (x == 6).sum())
        )
        .reset_index()
    )

    team_boundary["Total_Boundaries"] = (
        team_boundary["Fours"] + team_boundary["Sixes"]
    )

    team_boundary = team_boundary.sort_values(
        "Total_Boundaries",
        ascending=False
    )

    # -------------------------------
    # Plotly Graph
    # -------------------------------

    fig = go.Figure()

    # Fours
    fig.add_trace(
        go.Bar(
            x=team_boundary["batting_team"],
            y=team_boundary["Fours"],
            name="Fours",
            marker_color="#2563EB",
            text=team_boundary["Fours"],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Fours: %{y}<extra></extra>"
        )
    )

    # Sixes
    fig.add_trace(
        go.Bar(
            x=team_boundary["batting_team"],
            y=team_boundary["Sixes"],
            name="Sixes",
            marker_color="#F59E0B",
            text=team_boundary["Sixes"],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Sixes: %{y}<extra></extra>"
        )
    )

    # Layout
    fig.update_layout(
        barmode="group",
        title=dict(
            text="🏏 Team Boundary Comparison — IPL 2026",
            x=0.5,
            font=dict(size=22),
            xanchor="center"
        ),
        template="plotly_dark",
        height=600,
        xaxis_title="Teams",
        yaxis_title="Boundary Count",
        legend_title="Boundary Type"
    )

    # Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    
    #______________________________________________________________________________________________________________________--
    
    #_________________________________________________________________________________________________________________
    
    # ---------------------------------------------------
    # Total Runs
    # ---------------------------------------------------

    df["total_runs"] = df["runs_of_bat"] + df["extras"]

    # ---------------------------------------------------
    # Legal Balls
    # ---------------------------------------------------

    team_rr = (
        df.groupby("batting_team")
        .apply(lambda x: pd.Series({
            "Total_Runs": x["total_runs"].sum(),
            "Legal_Balls": ((x["wide"] == 0) & (x["noballs"] == 0)).sum()
        }))
        .reset_index()
    )

    # Overs
    team_rr["Overs"] = team_rr["Legal_Balls"] / 6

    # Run Rate
    team_rr["Run_Rate"] = (
        team_rr["Total_Runs"] / team_rr["Overs"]
    ).round(2)

    # Sort
    team_rr = team_rr.sort_values("Run_Rate", ascending=False)

    # ---------------------------------------------------
    # Plot
    # ---------------------------------------------------

    fig = px.line(
        team_rr,
        x="batting_team",
        y="Run_Rate",
        markers=True,
        text="Run_Rate"
    )

    fig.update_traces(

        line=dict(
        color=" skyblue",
            width=4
        ),

        marker=dict(
            size=10,
            color="skyblue",
            line=dict(
                color="skyblue",
                width=2
            )
        ),

        textposition="top center",

        textfont=dict(
            color="white",
            size=12
        ),

        hovertemplate=
        "<b>%{x}</b><br>"
        "Run Rate : %{y:.2f}"
        "<extra></extra>"
    )

    fig.update_layout(

        title=dict(
            text="📈 Team Run Rate Comparison",
            x=0.5,
            font=dict(size=22),
            xanchor="center"
        ),

        template="plotly_dark",

        height=550,

        xaxis=dict(
            title="Batting Team",
            showgrid=False,
            tickfont=dict(size=13)
            
        ),

        yaxis=dict(
            title="Run Rate",
            gridcolor="rgba(255,255,255,0.08)",
            tickfont=dict(size=13)
        ),

        hovermode="x unified",

        showlegend=False,

        font=dict(
            family="Segoe UI",
            size=13,
            color="white"
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    
    #_____________________________________________________________________________________________________________
    
    
    # --------------------------------------------------
    # Average Runs by Match Phase
    # --------------------------------------------------

    # ------------------------------------
    # Total Runs Per Ball
    # ------------------------------------

    df["total_runs"] = df["runs_of_bat"] + df["extras"]

    # ------------------------------------
    # Over Number (0.1 -> 1, 5.6 -> 6)
    # ------------------------------------

    df["over_number"] = (
        df["over"]
        .astype(str)
        .str.split(".")
        .str[0]
        .astype(int)
        + 1
    )

    # ------------------------------------
    # Assign Match Phase
    # ------------------------------------

    def get_phase(over):
        if over <= 6:
            return "Powerplay"
        elif over <= 15:
            return "Middle Overs"
        else:
            return "Death Overs"

    df["phase"] = df["over_number"].apply(get_phase)

    # ------------------------------------
    # Runs in each innings for every phase
    # ------------------------------------

    phase_runs = (
        df.groupby(
            ["match_no", "innings", "batting_team", "phase"],
            as_index=False
        )
        .agg(Runs=("total_runs", "sum"))
    )

    # ------------------------------------
    # Average phase runs by team
    # ------------------------------------

    team_phase = (
        phase_runs.groupby(
            ["batting_team", "phase"],
            as_index=False
        )
        .agg(Average_Runs=("Runs", "mean"))
    )

    # ------------------------------------
    # Plotly Bar Chart
    # ------------------------------------

    fig = px.bar(
        team_phase,
        x="batting_team",
        y="Average_Runs",
        color="phase",
        barmode="group",
        text_auto=".1f",
        color_discrete_map={
            "Powerplay": "#1E88E5",
            "Middle Overs": "#43A047",
            "Death Overs": "#E53935"
        }
    )

    fig.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    fig.update_layout(
        title=dict(
            text="<b>🏏Average Runs by Match Phase — IPL 2026</b>",
            x=0.5,
            font=dict(size=22),
            xanchor="center"
            
        ),
        template="plotly_white",
        height=600,
        xaxis_title="<b>Team</b>",
        yaxis_title="<b>Average Runs</b>",
        legend_title="<b>Phase</b>",
        font=dict(size=14),
        xaxis=dict(tickangle=0),
        margin=dict(t=80, l=40, r=20, b=80)
    )

    st.plotly_chart(fig, width="stretch")
    
    #____________________________________________________________________________________________________________________
    
    # ----------------------------------------------------
    # Total Wickets Taken by Team
    # ----------------------------------------------------

    wickets_df = (
        df[
            (df["wicket_type"].notna()) &
            (~df["wicket_type"].isin(["run out", "retired hurt", "retired out"]))
        ]
        .groupby("bowling_team")
        .size()
        .reset_index(name="Wickets")
        .sort_values("Wickets", ascending=True)
        .reset_index(drop=True)
    )

    # ----------------------------------------------------
    # Marker Colors (Top 3 Highlight)
    # ----------------------------------------------------

    colors = ["#00D4FF"] * len(wickets_df)

    colors[-1] = "#FFD700"   # Gold
    colors[-2] = "#C0C0C0"   # Silver
    colors[-3] = "#CD7F32"   # Bronze

    # ----------------------------------------------------
    # Figure
    # ----------------------------------------------------

    fig = go.Figure()

    # Lollipop Sticks
    for i in range(len(wickets_df)):
        fig.add_shape(
            type="line",
            x0=0,
            y0=i,
            x1=wickets_df.loc[i, "Wickets"],
            y1=i,
            line=dict(
                color="rgba(255,255,255,0.35)",
                width=2.5
            )
        )

    # Lollipop Heads
    fig.add_trace(
        go.Scatter(
            x=wickets_df["Wickets"],
            y=wickets_df["bowling_team"],

            mode="markers+text",

            marker=dict(
                size=19,
                color=colors,
                line=dict(
                    color="white",
                    width=2
                )
            ),

            text=wickets_df["Wickets"],

            textposition="middle right",

            textfont=dict(
                size=15,
                color="white",
                family="Arial Black"
            ),

            hovertemplate=
            "<b>%{y}</b><br>"
            "Total Wickets : <b>%{x}</b>"
            "<extra></extra>",

            showlegend=False
        )
    )

    # ----------------------------------------------------
    # Layout
    # ----------------------------------------------------

    fig.update_layout(

        title=dict(
            text="<b>Total Wickets Taken by Teams — IPL 2026</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=22)
        ),

        template="plotly_white",

        height=620,

        xaxis=dict(
            title="<b>Total Wickets</b>",
            showgrid=True,
            gridcolor="rgba(255,255,255,0.08)",
            gridwidth=1,
            zeroline=False
        ),

        yaxis=dict(
            title="<b>Bowling Team</b>",
            showgrid=False
        ),

        hoverlabel=dict(
            bgcolor="#1E293B",
            bordercolor="white",
            font_size=14,
            font_family="Arial"
        ),

        font=dict(size=14),

        margin=dict(
            t=80,
            l=70,
            r=40,
            b=60
        )
    )

    st.plotly_chart(fig, width="stretch")
    
    #________________________________________________________________________________________________________________

    # ----------------------------------------------------
    # 🎳 Extras Conceded by Bowling Teams — IPL 2026
    # ----------------------------------------------------

    # -----------------------------------------
    # Extras by Bowling Teams
    # -----------------------------------------

    extras_df = (
        df.groupby("bowling_team")
        .agg(
            Wides=("wide", "sum"),
            No_Balls=("noballs", "sum"),
            Byes=("byes", "sum"),
            Leg_Byes=("legbyes", "sum")
        )
        .reset_index()
    )

    extras_df["Total"] = (
        extras_df["Wides"]
        + extras_df["No_Balls"]
        + extras_df["Byes"]
        + extras_df["Leg_Byes"]
    )

    # Sort by Total Extras
    extras_df = extras_df.sort_values("Total", ascending=False)

    # -----------------------------------------
    # Plot
    # -----------------------------------------

    fig = go.Figure()

    # Wides
    fig.add_bar(
        x=extras_df["bowling_team"],
        y=extras_df["Wides"],
        name="Wides",
        marker_color="#EF4444"
    )

    # No Balls
    fig.add_bar(
        x=extras_df["bowling_team"],
        y=extras_df["No_Balls"],
        name="No Balls",
        marker_color="#F59E0B"
    )

    # Byes
    fig.add_bar(
        x=extras_df["bowling_team"],
        y=extras_df["Byes"],
        name="Byes",
        marker_color="#3B82F6"
    )

    # Leg Byes
    fig.add_bar(
        x=extras_df["bowling_team"],
        y=extras_df["Leg_Byes"],
        name="Leg Byes",
        marker_color="#22C55E"
    )

    # -----------------------------------------
    # Total Labels
    # -----------------------------------------

    fig.add_trace(
        go.Scatter(
            x=extras_df["bowling_team"],
            y=extras_df["Total"] + 3,
            mode="text",
            text=extras_df["Total"],
            textfont=dict(
                size=15,
                color="white",
                family="Arial Black"
            ),
            showlegend=False,
            hoverinfo="skip"
        )
    )

    # -----------------------------------------
    # Layout
    # -----------------------------------------

    fig.update_layout(
        
         title=dict(
        text="<b> 🎳 Extras Conceded by Bowling Teams — IPL 2026</b>",
        x=0.5,
        xanchor="center",
        font=dict(size=22)
    ),

        barmode="stack",

        template="plotly_white",

        height=620,

        xaxis=dict(
            title="<b>Bowling Team</b>",
            tickfont=dict(
                size=13,
                family="Arial Black"
            )
        ),

        yaxis=dict(
            title="<b>Total Extras</b>",
            showgrid=True,
            gridcolor="rgba(180,180,180,0.25)",
            gridwidth=1,
            range=[0, extras_df["Total"].max() + 20]
        ),

        legend=dict(
            orientation="h",
            y=-0.18,
            x=0.5,
            xanchor="center",
            title="<b>Extra Type</b>",
            font=dict(size=13)
        ),

        hovermode="x unified",

        margin=dict(
            t=70,
            b=60,
            l=60,
            r=40
        ),

        font=dict(size=14)
    )

    # -----------------------------------------
    # Hover Template
    # -----------------------------------------

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>"
    )

    # -----------------------------------------
    # Streamlit Chart
    # -----------------------------------------

    st.plotly_chart(fig, width="stretch")