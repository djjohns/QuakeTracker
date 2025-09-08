import requests
import pandas as pd
import plotly.graph_objects as go

# USGS feeds
feeds = {
    "Past Day (≥2.5)": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson",
    "Past Week (≥2.5)": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson",
    "Past Month (≥2.5)": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson",
}

# Fetch and prepare DataFrames
dfs = {}
for label, url in feeds.items():
    features = requests.get(url).json()["features"]
    quakes = [
        {
            "Place": q["properties"]["place"],
            "Mag": q["properties"]["mag"],
            "Lat": q["geometry"]["coordinates"][1],
            "Lon": q["geometry"]["coordinates"][0],
        }
        for q in features
        if q["properties"]["mag"] is not None  # guard against None magnitudes
    ]
    dfs[label] = pd.DataFrame(quakes)

# Build traces and buttons
traces = []
buttons = []
labels = list(dfs.keys())

for i, label in enumerate(labels):
    df = dfs[label]

    traces.append(
        go.Scattergeo(
            lat=df["Lat"],
            lon=df["Lon"],
            text=[
                f"{place}<br>Mag: {mag:.1f}"
                for place, mag in zip(df["Place"], df["Mag"])
            ],
            hovertemplate="%{text}<extra></extra>",
            marker=dict(
                size=df["Mag"] * 50,
                color=df["Mag"],
                colorscale="Viridis",
                colorbar=dict(title="Magnitude"),
                sizemode="area",
                opacity=0.85,
            ),
            name=label,
            visible=(i == 0),  # only first visible initially
        )
    )

    vis = [False] * len(labels)
    vis[i] = True

    # Only update title so the dropdown stays intact.
    buttons.append(
        dict(
            label=label,
            method="update",
            args=[
                {"visible": vis},
                {"title.text": f"🌎 Recent Earthquakes — {label}"},
            ],
        )
    )

# Create figure
fig = go.Figure(data=traces)

# Style layout once (do NOT reassign updatemenus from button actions)
fig.update_layout(
    template="plotly_dark",
    title=dict(
        text="🌎 Recent Earthquakes — Past Day (≥2.5)",
        font=dict(color="cyan", size=22),
        x=0.5,
        xanchor="center",
        y=0.95,
        yanchor="top",
    ),
    margin=dict(t=90, r=20, l=20, b=20),
    geo=dict(
        projection_type="natural earth",
        bgcolor="rgba(0,0,0,0)",
        landcolor="rgb(40,40,40)",
        oceancolor="rgb(10,10,40)",
        showocean=True,
        showcountries=True,
    ),
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=0.01,
            y=1.12,
            xanchor="left",
            yanchor="top",
            pad=dict(r=8, t=8, b=8, l=8),
            bgcolor="rgba(40,40,40,0.7)",
            bordercolor="rgba(255,255,255,0.2)",
        )
    ],
)

fig.show()
