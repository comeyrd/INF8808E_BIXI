import plotly.graph_objects as go
import pandas as pd

def generate_bar_chart_daily_traffic(station_id, day_chart_df, station_name):
    df_station = day_chart_df[day_chart_df['station_id_s'] == station_id].copy()

    # S'assurer que la date est bien en format datetime
    df_station['day_date'] = pd.to_datetime(df_station['day_date'])

    # Extraire le jour de la semaine (0 = lundi, ..., 6 = dimanche)
    df_station['jour_semaine'] = df_station['day_date'].dt.dayofweek

    # Mapper les jours à des noms lisibles
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    couleurs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']  # couleurs par jour

    df_station['jour_nom'] = df_station['jour_semaine'].map(lambda x: jours[x])

    # Grouper et sommer le nombre de passages
    df_grouped = df_station.groupby('jour_nom')['nb_passages'].sum().reindex(jours)

    # Créer le bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_grouped.index,
        y=df_grouped.values,
        marker_color=couleurs,
        hovertemplate="<b>%{x}</b><br>Passages : %{y:,.0f}<extra></extra>"
    ))

    fig.update_layout(
        title=f"Trafic total par jour de la semaine – {station_name}",
        xaxis_title="Jour de la semaine",
        yaxis_title="Nombre total de passages",
        template='plotly_white'
    )

    return fig
