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
        xgap=2,  # séparation horizontale
        ygap=2   # séparation verticale
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

    # Ajouter rectangle de sélection
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

    jours = heatmap_data.index
    semaines = heatmap_data.columns

    # Créer une matrice mois[jour, semaine]
    mois_matrix = {
        (jour, semaine): df_day[
            (df_day["Semaine"] == semaine) & (df_day["JourSemaineStr"] == jour)
        ]["Mois"].mode().iloc[0] if not df_day[
            (df_day["Semaine"] == semaine) & (df_day["JourSemaineStr"] == jour)
        ]["Mois"].mode().empty else None
        for jour in jours for semaine in semaines
    }

    # 🔲 Tracer les barres verticales (séparation mois entre semaines)
    for i in range(1, len(semaines)):
        curr_week = semaines[i]
        prev_week = semaines[i - 1]
        for j, jour in enumerate(jours):
            mois_curr = mois_matrix.get((jour, curr_week))
            mois_prev = mois_matrix.get((jour, prev_week))
            if mois_curr != mois_prev:
                # Ligne verticale pour ce jour uniquement
                fig.add_shape(
                    type="line",
                    x0=curr_week - 0.5,
                    x1=curr_week - 0.5,
                    y0=j - 0.5,
                    y1=j + 0.5,
                    xref='x',
                    yref='y',
                    line=dict(color="black", width=2)
                )

    # 🔲 Tracer les barres horizontales (séparation mois entre jours)
    for j in range(1, len(jours)):
        curr_jour = jours[j]
        prev_jour = jours[j - 1]
        for i, semaine in enumerate(semaines):
            mois_curr = mois_matrix.get((curr_jour, semaine))
            mois_prev = mois_matrix.get((prev_jour, semaine))
            if mois_curr != mois_prev:
                # Ligne horizontale pour cette semaine uniquement
                fig.add_shape(
                    type="line",
                    x0=semaine - 0.5,
                    x1=semaine + 0.5,
                    y0=j - 0.5,
                    y1=j - 0.5,
                    xref='x',
                    yref='y',
                    line=dict(color="black", width=2)
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


