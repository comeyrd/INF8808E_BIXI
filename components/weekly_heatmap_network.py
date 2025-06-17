import pandas as pd
import plotly.express as px
from shapely.geometry import box
from shapely.ops import unary_union


def generate_weekly_network_heatmap(df_day, selected_week=None):
    heatmap_data = df_day.pivot_table(
        index="JourSemaineStr",  # lignes = jours de semaine
        columns="Semaine",       # colonnes = semaines
        values="nb_passages",
        aggfunc="sum",
        fill_value=0,
        observed=False)
    
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

    # ✅ Ajouter des espaces entre les jours
    fig.update_xaxes(showline=False, tickmode="array", tickvals=heatmap_data.columns)
    fig.update_yaxes(tickmode="array", tickvals=list(range(len(heatmap_data.index))), ticktext=heatmap_data.index)
    fig.update_traces(xgap=2, ygap=2)  # ESPACEMENT horizontal & vertical entre les cases
    fig.update_yaxes(scaleanchor="x", scaleratio=1)


    # ✅ Axe Y : jours abrégés
    fig.update_yaxes(
        title=None,
        tickmode="array",
        tickvals=list(range(len(heatmap_data.index))),
        ticktext=heatmap_data.index,
        showgrid=False
    )


    # ✅ Axe X : afficher les mois centrés
    mois_ticks = df_day.groupby("Mois")["Semaine"].median().astype(int)
    mois_labels = df_day.groupby("Mois")["MoisStr"].first()

    fig.update_xaxes(
        tickmode="array",
        tickvals=mois_ticks,
        ticktext=mois_labels,
        title=None,
        showgrid=False
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
            line=dict(color='black', width=2),
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

    fig.update_traces(hovertemplate=None, hoverinfo='skip')


    return fig


