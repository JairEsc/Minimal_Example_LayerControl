import json

import dash_leaflet as dl
from dash import Dash, html, Output, Input
import geopandas as gpd
# Some shapes.
gdf_shapefile=gpd.read_file('assets/municipiosjair.shp')
gdf_shapefile2=gpd.read_file('assets/mercados_corregidos.shp')
# Crear la estructura GeoJSON con tooltips
#print(gdf_shapefile.Area)
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": feature["geometry"],
            "properties": {
                **feature["properties"],
            }
        }
        for idx, feature in enumerate(gdf_shapefile.__geo_interface__["features"])
    ]
}
geojson_data2 = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": feature["geometry"],
            "properties": {
                **feature["properties"],
            }
        }
        for idx, feature in enumerate(gdf_shapefile2.__geo_interface__["features"])
    ]
}





#
markers = [dl.Marker(position=[56, 10]), dl.CircleMarker(center=[55, 10], radius=50)]
polygon = dl.Polygon(positions=[[57, 10], [57, 11], [56, 11], [57, 10]])
# Some tile urls.
keys = ["toner", "terrain"]
url_template = "http://{{s}}.tile.stamen.com/{}/{{z}}/{{x}}/{{y}}.png"
attribution = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, ' \
              '<a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data ' \
              '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
# Create app.
layerControl=dl.LayersControl(
            [dl.BaseLayer([dl.GeoJSON(data=geojson_data)],
                          name="A",),
            dl.BaseLayer([dl.GeoJSON(data=geojson_data2)],
                          name="B",checked=True)]+[dl.TileLayer(),dl.TileLayer()], id="lc"
        )

app = Dash()
app.layout = html.Div([
    dl.Map([
        # dl.LayersControl(
        #     [dl.BaseLayer(dl.TileLayer(url=url_template.format(key)),
        #                   name=key, checked=key == "toner") for key in keys], id="lc"
        # )
        layerControl
    ], zoom=7, center=(20, -98), style={'height': '50vh'}),
    html.Div(id="log")
])

@app.callback(Output("log", "children"), Input("lc", "baseLayer"),
              Input("lc", "overlays"), prevent_initial_call=True)
def log(base_layer, overlays):
    return f"Base layer is {base_layer}, selected overlay(s): {json.dumps(overlays)}"

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)