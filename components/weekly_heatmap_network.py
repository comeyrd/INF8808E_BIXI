import pandas as pd
import plotly.express as px
from shapely.geometry import box
from shapely.ops import unary_union
import plotly.graph_objects as go
import numpy as np


def generate_weekly_network_heatmap(df_day, heatmap_data, mois_matrix, selected_week=None):

    z = heatmap_data.values.astype(float)
    z[z == 0] = np.nan

    # Générer les étiquettes de date
    jours = heatmap_data.index
    semaines = heatmap_data.columns

    # Créer une table des dates lisibles
    jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    mois_fr = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
               "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

    label_matrix = []
    for jour in jours:
        row_labels = []
        for semaine in semaines:
            sous_df = df_day[(df_day["WeekIndex"] == semaine) & (df_day["JourStr"] == jour)]
            if not sous_df.empty:
                r = sous_df.iloc[0]
                label = f"{jours_fr[r['Jour']]} {r['JourNum']} {mois_fr[r['Mois'] - 1]}"
            else:
                label = ""
            row_labels.append(label)
        label_matrix.append(row_labels)

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=semaines,
        y=jours,
        customdata=label_matrix,
        colorscale='Reds',
        hovertemplate="<b>Date :</b> %{customdata}<br><b>Passages :</b> %{z:,.0f} passages<extra></extra>",
        showscale=True,
        xgap=2,
        ygap=2,
        zmin=np.nanmin(z),
        zmax=np.nanmax(z),
        coloraxis="coloraxis",
    ))

    shapes = []
    for i in range(1, len(semaines)):
        curr_week = semaines[i]
        prev_week = semaines[i - 1]
        for j, jour in enumerate(jours):
            mois_curr = mois_matrix.at[jour, curr_week]
            mois_prev = mois_matrix.at[jour, prev_week]
            if mois_curr != mois_prev:
                shapes.append(dict(
                    type="line",
                    x0=curr_week - 0.5,
                    x1=curr_week - 0.5,
                    y0=j - 0.5,
                    y1=j + 0.5,
                    xref='x',
                    yref='y',
                    line=dict(color="black", width=2)
                ))

    for j in range(1, len(jours)):
        curr_jour = jours[j]
        prev_jour = jours[j - 1]
        for i, semaine in enumerate(semaines):
            mois_curr = mois_matrix.at[curr_jour, semaine]
            mois_prev = mois_matrix.at[prev_jour, semaine]
            if mois_curr != mois_prev:
                shapes.append(dict(
                    type="line",
                    x0=semaine - 0.5,
                    x1=semaine + 0.5,
                    y0=j - 0.5,
                    y1=j - 0.5,
                    xref='x',
                    yref='y',
                    line=dict(color="black", width=2)
                ))

    fig.update_layout(shapes=shapes)

    # --- TICKS MOIS ---
    mois_fr_abbr = ["Jan", "Fév", "Mars", "Avr", "Mai", "Juin",
                    "Juil", "Août", "Sept", "Oct", "Nov", "Déc"]

    mois_ticks = df_day.groupby("Mois")["WeekIndex"].median().astype(int)
    mois_labels = mois_ticks.index.map(lambda m: mois_fr_abbr[m - 1])
    
    fig.update_layout(
        title_text="Fréquentation quotidienne du réseau cyclable en 2024",
        title_x=0.5,
        title_font=dict(size=20),
        xaxis=dict(
            title="",
            showgrid=False,
            tickmode="array",
            tickvals=mois_ticks.tolist(),
            ticktext=mois_labels.tolist(),
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

    # Forcer 0 comme borne inférieure et amplifier légèrement la borne supérieure
    y_max = agg["nb_passages"].max() * 1.05

    fig.update_layout(
        title=None,
        xaxis_title=None,
        yaxis_title="Nombre de passages",
        coloraxis_showscale=False,
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            range=[0, y_max]  # 0 est forcé ici
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    fig.update_traces(
        hovertemplate='%{x}<br>Passages : %{y:,.0f} passages',
        texttemplate='%{text:,}',
        textposition='outside'
    )

    return fig
