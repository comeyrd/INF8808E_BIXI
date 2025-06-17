import pandas as pd
import plotly.express as px
from shapely.geometry import box
from shapely.ops import unary_union


# Préparer les données dès le chargement
df_raw = pd.read_csv("data/bixi_comptage_day_2024.csv")
jours_fr_abbr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
mois_fr = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Aoû", "Sep", "Oct", "Nov", "Déc"]

df_raw["Date"] = pd.to_datetime(df_raw["day"], unit="ms")
df_raw["WeekIndex"] = (df_raw["Date"] - pd.Timestamp("2024-01-01")).dt.days // 7
df_raw["Count"] = df_raw["nb_passages"]
df_raw["Semaine"] = df_raw["Date"].dt.isocalendar().week + 1
# Préparer les données une seule fois
df = df_raw.copy()
df["JourSemaine"] = df["Date"].dt.weekday  # 0 = lundi
df["JourSemaineStr"] = pd.Categorical(
    df["JourSemaine"].map(lambda i: jours_fr_abbr[i]),
    categories=jours_fr_abbr,
    ordered=True
)

df["Mois"] = df["Date"].dt.month
df["MoisStr"] = df["Mois"].map(lambda i: mois_fr[i - 1])
df["Jour"] = df["Date"].dt.day
df["Colonne"] = (df["Date"] - pd.to_datetime("2024-01-01")).dt.days  # un jour = une colonne
df["Passages"] = df["nb_passages"]

heatmap_data = df.pivot_table(
    index="JourSemaineStr",  # lignes = jours de semaine
    columns="Semaine",       # colonnes = semaines
    values="Passages",
    aggfunc="sum"
)

def generate_weekly_network_heatmap(selected_week=None):
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
    mois_ticks = df.groupby("Mois")["Semaine"].median().astype(int)
    mois_labels = df.groupby("Mois")["MoisStr"].first()

    fig.update_xaxes(
        tickmode="array",
        tickvals=mois_ticks,
        ticktext=mois_labels,
        title=None,
        showgrid=False
    )

    fig.update_layout(
        
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

    fig.update_traces(hovertemplate=None, hoverinfo='skip')


    return fig


