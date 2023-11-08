from plotly.express import line, bar_polar, choropleth_mapbox
from plotly.express.colors import sequential
from pandas import DataFrame, to_datetime
from plotly.offline import plot
import json


def generate_date_speed_graph(data):
    df = DataFrame(data)
    df['date'] = to_datetime(df['date'])
    df.rename(columns={'date': 'Fecha', 'speed': 'Velocidad'}, inplace=True)
    fig = line(df, x='Fecha', y='Velocidad')
    plotly_url = plot(fig, filename='./static/bar.html', auto_open=False)

def df_to_geojson(df):
    df = DataFrame(df)
    geojson = {'type': 'FeatureCollection', 'features': []}

    for i, element in df.iterrows():
        feature = {
            'type': 'Feature', 
            'properties': {},
            'geometry': {}
        }
        
        feature['geometry'] = json.loads(element['geometry'])
        if 'Nariño' in element['name']:
                feature['properties']['name'] = 'Narino'
        elif 'bogota' in element['name']:
            feature['properties']['name'] = 'Bogota d.c'
        else:
            feature['properties']['name'] = element['name']
        feature['properties']['area'] = element['area']
        feature['properties']['perimeter'] = element['perimeter']
        feature['properties']['hectares'] = element['hectares']
        geojson['features'].append(feature)
    return geojson

def generate_rose_diagram(DIRECTIONS, data):
    data = [*map(lambda x: {'name': x['name'], 'medianSpeed': x['medianSpeed'], 'medianDirection': DIRECTIONS[(int((x['medianDirection']/22.5) + .5) % 16)]}, data)]
    data += [{'name': '', 'medianSpeed': 0, 'medianDirection': d} for d in DIRECTIONS]
    data = [tuple for x in DIRECTIONS for tuple in data if tuple['medianDirection'] == x]
    df = DataFrame(data)
    df.rename(columns={'name': 'Nombre', 'medianSpeed': 'Velocidad', 'medianDirection': 'Dirección'}, inplace=True)        
    fig = bar_polar(
        df, 
        r='Velocidad', 
        theta='Dirección', 
        color='Nombre', 
        color_discrete_sequence=sequential.Plasma_r
    )
    fig.update_layout(
            font_family = "Rockwell",
            legend = dict(
                title = None, 
                orientation = "h", 
                y = 1, 
                yanchor = "bottom", 
                x = 0.5, 
                xanchor = "center"
            )
        )
    return fig.to_html()

def generate_map_graph(geo_data, data):
        geo_json = df_to_geojson(geo_data)
        df = DataFrame(data)
        df['name'] = df['name'].str.capitalize()
        df.rename(columns={'name': 'Nombre'}, inplace=True)
        fig = choropleth_mapbox(
            df, 
            geojson = geo_json, 
            locations = 'Nombre',
            featureidkey = 'properties.name',
            color = 'medianSpeed',
            color_continuous_scale = "Viridis",
            range_color = (df['medianSpeed'].min(), df['medianSpeed'].max()),
            mapbox_style = "carto-positron",
            zoom = 4,
            center = {"lat": 3.5495372146017536, "lon": -73.04261938707367},
            opacity=  0.5,
            labels = {'medianSpeed': 'Velocidad'}
        )
        fig.update_layout(
            font_family = "Rockwell"
        )
        return fig.to_html()