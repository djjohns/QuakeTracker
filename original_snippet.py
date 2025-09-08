import requests
import pandas as pd
import plotly.express as px


#  Magnitude ≥ 2.5 Past Day
url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson"

data = requests.get(url).json()["features"]

quakes = [
    {
        "Place": q["properties"]["place"],
        "Mag": q["properties"]["mag"],
        "Lat": q["geometry"]["coordinates"][1],
        "Lon": q["geometry"]["coordinates"][0],
    }
    for q in data
]

df = pd.DataFrame(quakes)

fig = px.scatter_geo(
    df,
    lat="Lat",
    lon="Lon",
    color="Mag",
    size="Mag",
    title="🌎 Recent Earthquakes (Magnitude ≥ 2.5, Past Day)",
    projection="natural earth",
)

fig.show()
