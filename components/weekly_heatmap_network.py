import pandas as pd
import plotly.express as px
import numpy as np


def generate_weekly_network_heatmap(df_raw,selected_week=None):
    fig = px.density_heatmap(
        df_raw,
        x="WeekIndex",
        y="Weekday",
        z="Count",
        color_continuous_scale="Reds",
        labels={"WeekIndex": "Semaine", "Weekday": "Jour", "Count": ""},
    )
    fig.update_yaxes(
        tickmode="array",
        tickvals=list(range(7)),
        #icktext=["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    )
    fig.update_layout(
        title="Fréquentation journalière",
        dragmode=False,
        yaxis_title=None,
        yaxis=dict(
            showticklabels=False
        ),
        coloraxis_colorbar=dict(title="Nombre de passages")
    )

    if selected_week is not None:
        fig.add_shape(
            type="rect",
            x0=selected_week - 0.5,
            x1=selected_week + 0.5,
            y0=-0.5,
            y1=6.5,
            xref='x',
            yref='y',
            line=dict(color='black', width=3),
            fillcolor='rgba(0,0,0,0)',  # transparent
            layer='above'
        )
    return fig

def generate_bar_chart(week_index):
    # Filtrer uniquement la semaine sélectionnée
    d = df_raw[df_raw["WeekIndex"] == week_index].copy()
    if d.empty:
        return px.bar(title=f"Aucune donnée pour la semaine {week_index}")

    # Traduire les jours en français
    jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    d["Weekday"] = d["Date"].dt.weekday
    d["JourNum"] = d["Date"].dt.strftime("%d")
    d["WeekdayName"] = d["Weekday"].map(lambda i: jours_fr[i]) + " " + d["JourNum"]

    # Agréger : somme des passages par jour
    agg = (
        d.groupby(["Weekday", "WeekdayName"])["Count"]
        .sum()
        .reset_index()
        .sort_values("Weekday")
    )

    # Bar chart
    fig = px.bar(
        agg,
        x="WeekdayName",
        y="Count",
        color="Count",
        text="Count",
        color_continuous_scale="Reds",
        title=None
    )

    fig.update_layout(
        title=None,
        xaxis_title=None,
        yaxis_title=None,
        coloraxis_showscale=False,
        yaxis=dict(
            showgrid=False,
            showticklabels=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    return fig


