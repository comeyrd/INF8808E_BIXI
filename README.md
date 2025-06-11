# Projet Bixi 

Structure des fichiers : 
```
.
├── components/
│   ├── montreal_interactive_map.py
│   ├── daily_heatmap_station.py
│   ├── line_chart_traffic_evolution.py
│   ├── bar_chart_nearby_stations.py
│   ├── radar_chart_district_comparison.py
│   ├── weekly_heatmap_network.py
│   └── animated_bixi_heatmap.py
├── layouts/
│   ├── page1.py
│   ├── page2.py
│   └── page3.py
├── templates/
│   └── project_theme.py
├── data_preprocessing.py
├── app.py
├── requirements.txt
└── server.py
```


- **montreal_interactive_map.py**: La carte principale de Montréal (affichant les pistes cyclables, les stations de comptage et les stations BIXI).
- **daily_heatmap_station.py**: Heatmap de fréquentation journalière par station (Sous-Visualisation 1.3).
line_chart_traffic_evolution.py: Graphique linéaire d'évolution du trafic cyclable sur l'année (Sous-Visualisation 1.1).
- **bar_chart_nearby_stations.py**: Graphique à barres de comparaison du trafic des stations proches (Sous-Visualisation 1.2).
- **radar_chart_district_comparison.py**: Radar chart pour comparer les différents quartiers de Montréal (Page 2).
- **weekly_heatmap_network.py**: Heatmap de fréquentation journalière du réseau entier sur l’année (Sous-Visualisation 3.1).
- **animated_bixi_heatmap.py**: Carte animée du nombre hebdomadaire de passages enregistrés par station BIXI à Montréal (Sous-Visualisation 3.2).


Dans chaque Fichier component, il y a une fonction pour créer le plot, et comme dans les TP il faut créer les autres fonctions pour faires des updates et des modifications
Ex 
```python
def generate_nom_viz(dataframe,autres_params):
    #CODE
    return fig

def update_nom_viz_propriete(fig,autre_param):
    #Do smth to fig
    return fig
```

Pour le dataframe en input de la creation de la dataviz, il faut faire le preprocessing dans le fichier data_preprocessing.py et l'appeler dans le fonction de la page avant d'appeler la figure
