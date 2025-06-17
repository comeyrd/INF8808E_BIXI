import pandas as pd
import plotly.express as px
from shapely.geometry import box
from shapely.ops import unary_union
import plotly.graph_objects as go


def generate_weekly_network_heatmap(df_day, heatmap_data, ticks, labels, selected_week=None):
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Reds',
        hovertemplate="<br>Jour : %{y}<br>Passages : %{z}<extra></extra>",
        showscale=True,
        xgap=2,
        ygap=2
    ))

    fig.update_layout(
        title_text="Fréquentation quotidienne du réseau cyclable en 2024",
        title_x=0.5,
        title_font=dict(size=20),
        xaxis=dict(
            title="",
            showgrid=False,
            tickmode="array",
            tickvals=list(ticks.values()),
            ticktext=list(labels.values()),
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
            line=dict(color='black', width=2),
            fillcolor='rgba(0,0,0,0)',
            layer='above'
        )

    return fig


def generate_bar_chart(df_day, week_number):
    d = df_day[df_day["Semaine"] == week_number].copy()
    if d.empty:
        return px.bar(title=f"Aucune donnée pour la semaine {week_number}")

    jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    d["Weekday"] = d["Date"].dt.weekday
    d["JourNum"] = d["Date"].dt.strftime("%d")
    d["WeekdayName"] = d["Weekday"].map(lambda i: jours_fr[i]) + " " + d["JourNum"]

    agg = (
        d.groupby(["Weekday", "WeekdayName"])["Count"]
        .sum()
        .reset_index()
        .sort_values("Weekday")
    )

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
