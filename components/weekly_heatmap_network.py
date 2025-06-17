import pandas as pd
import plotly.express as px
from shapely.geometry import box
from shapely.ops import unary_union
import plotly.graph_objects as go


def generate_weekly_network_heatmap(df_day, heatmap_data, ticks, labels, selected_week=None):

    fig = px.imshow(
        heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale="Reds",
        labels=dict(color="Passages"),
        aspect="auto"
    )


    fig.update_layout(
        xaxis_title="", yaxis_title="",
        plot_bgcolor='white', paper_bgcolor='white',
        coloraxis_colorbar=dict(title=None),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        title_text="Fréquentation quotidienne du réseau cyclable en 2024",
        title_x=0.5,
        title_font=dict(size=20),
        dragmode=False,
        
    )

    fig.update_traces(xgap=2, ygap=1, dx=1, dy=1)  # ESPACEMENT horizontal & vertical entre les cases

    fig.update_yaxes(
        title=None,
        tickmode="array",
        tickvals=list(range(len(heatmap_data.index))),
        ticktext=heatmap_data.index,
        showgrid=False,
        scaleanchor="x",
        scaleratio=1
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=list(ticks.values()),
        ticktext=list(labels.values()),
        showline=False
    )


    # ✅ Rectangle ajusté à une colonne (case)
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


def generate_bar_chart(df_day, week_index):
    # Filtrer uniquement la semaine sélectionnée
    d = df_day[df_day["WeekIndex"] == week_index].copy()
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

    fig.update_traces(
        hoverinfo='skip',
        selector=dict(type='heatmap')
    )


    return fig


