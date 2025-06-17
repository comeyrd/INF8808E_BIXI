import pandas as pd
import plotly.express as px
from shapely.geometry import box
from shapely.ops import unary_union
import plotly.graph_objects as go
import numpy as np


def generate_weekly_network_heatmap(df_day, heatmap_data, mois_separateurs, selected_week=None):
    z = heatmap_data.values.astype(float)  # Assure un tableau float
    z[z == 0] = np.nan  # Ignore les zéros dans l'affichage

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Reds',
        hovertemplate="<br>Jour : %{y}<br>Passages : %{z}<extra></extra>",
        showscale=True,
        xgap=2,
        ygap=2,
        zmin=np.nanmin(z),  # Échelle basée uniquement sur les vraies valeurs
        zmax=np.nanmax(z)
    ))
    
    for x_pos in mois_separateurs:
        fig.add_shape(
            type="line",
            x0=x_pos, x1=x_pos,
            y0=-0.5, y1=6.5,
            line=dict(color="black", width=2),
            xref="x", yref="y"
        )

    fig.update_layout(
        title_text="Fréquentation quotidienne du réseau cyclable en 2024",
        title_x=0.5,
        title_font=dict(size=20),
        xaxis=dict(
            title="",
            showgrid=False,
            tickangle=45,        # Incliner les labels pour éviter le chevauchement
            automargin=True,
            showline=False
        ),
        yaxis=dict(
            title="",
            tickmode="array",
            tickvals=list(range(len(heatmap_data.index))),
            ticktext=heatmap_data.index,
            showgrid=False,
            scaleanchor="x",
            scaleratio=1
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        dragmode=False
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
            line=dict(color='black', width=4),
            fillcolor='rgba(0,0,0,0)',
            layer='above'
        )

    return fig


def generate_bar_chart(df_day, week_number, gloabal_max=100, gloabal_min=0):
    d = df_day[df_day["WeekIndex"] == week_number].copy()
    if d.empty:
        return px.bar(title=f"Aucune donnée pour la semaine {week_number}")
    
    jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    mois_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
            "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    d["x_label"] = d.apply(
        lambda row: f"{jours_fr[row['Jour']]} {row['JourNum']} {mois_fr[row['Mois'] - 1]}", axis=1
    )
    
    agg = (
        d.groupby(["Jour", "x_label"])["nb_passages"]
        .sum()
        .reset_index()
        .sort_values("Jour")
    )

    fig = px.bar(
        agg,
        x="x_label",
        y="nb_passages",
        color="nb_passages",
        text="nb_passages",
        color_continuous_scale="Reds",
        range_color=[gloabal_min, gloabal_max],
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

    fig.update_traces(
        hoverinfo='skip',
        selector=dict(type='heatmap')
    )

    return fig
