import json
from pathlib import Path

import folium
import streamlit as st
from streamlit_folium import st_folium

DATA = Path(__file__).resolve().parent.parent / "data" / "output" / "buildings.geojson"
COLORS = {
    "red": "#d73027",
    "orange": "#fc8d59",
    "yellow": "#fee08b",
    "green": "#1a9850",
    None: "#9e9e9e",
}
LABELS = {
    "red": "Destroyed",
    "orange": "Priority inspection",
    "yellow": "Monitor",
    "green": "Nothing urgent",
    None: "Not assessed",
}
FIELDS = [
    ("building_id", "ID"),
    ("triage_status", "Triage"),
    ("area_m2", "Area (m2)"),
    ("levels", "Levels"),
    ("height_m", "Height (m)"),
    ("epoch", "Built"),
    ("typology", "Typology"),
    ("vuln_score", "Vulnerability"),
    ("damage_score", "Damage score"),
    ("unosat_label", "UNOSAT label"),
    ("exposure_score", "Exposure"),
    ("cost_estimate_usd", "Cost estimate (USD)"),
]


@st.cache_data
def load_buildings(path):
    return json.loads(Path(path).read_text())


def style(feature):
    status = feature["properties"]["triage_status"]
    return {"fillColor": COLORS[status], "color": "#333333", "weight": 1, "fillOpacity": 0.8}


def build_map(collection):
    feats = collection["features"]
    lons = [c[0] for f in feats for c in f["geometry"]["coordinates"][0]]
    lats = [c[1] for f in feats for c in f["geometry"]["coordinates"][0]]
    m = folium.Map(tiles="OpenStreetMap")
    m.fit_bounds(
        [[min(lats), min(lons)], [max(lats), max(lons)]],
        padding=(20, 20),
    )
    folium.GeoJson(
        {"type": "FeatureCollection", "features": feats},
        style_function=style,
        highlight_function=lambda f: {"weight": 3, "color": "#000000"},
        tooltip=folium.GeoJsonTooltip(fields=["building_id", "triage_status"], aliases=["ID", "Triage"]),
    ).add_to(m)
    return m


def building_card(props):
    st.subheader(props["building_id"])
    st.markdown(f"**{LABELS[props['triage_status']]}**")
    for key, label in FIELDS[1:]:
        value = props[key]
        st.write(f"{label}: {'n/a' if value is None else value}")


def main():
    st.set_page_config(page_title="re:build", layout="wide")
    st.title("re:build")
    collection = load_buildings(DATA)
    statuses = sorted({f["properties"]["triage_status"] or "none" for f in collection["features"]})
    chosen = st.sidebar.multiselect("Triage status", statuses, default=statuses)
    feats = [
        f
        for f in collection["features"]
        if (f["properties"]["triage_status"] or "none") in chosen
    ]
    if not feats:
        st.info("Nicio clădire nu corespunde filtrelor selectate.")
        return
    left, right = st.columns([3, 1])
    with left:
        result = st_folium(
            build_map({"features": feats}),
            height=560,
            use_container_width=True,
            returned_objects=["last_object_clicked_tooltip"],
        )
    with right:
        clicked = (result or {}).get("last_object_clicked_tooltip")
        match = None
        if clicked:
            for f in feats:
                if f["properties"]["building_id"] in clicked:
                    match = f["properties"]
        if match:
            building_card(match)
        else:
            st.info("Click a building to see its card.")


main()
