from plotly.express import bar, bar_polar, choropleth_mapbox
from plotly.express.colors import sequential
from pandas import DataFrame, to_datetime
from django.conf import settings
from plotly.offline import plot
import json, os


def generate_hour_speed_graph(data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    df = DataFrame(data)
    df.rename(columns={'hour': 'Hora', 'avgSpeed': 'Promedio', 'medSpeed': 'Mediana'}, inplace=True)
    fig = bar(
        df, 
        x='Hora', 
        y=['Promedio', 'Mediana'], 
        barmode = 'group'
    )
    fig.update_layout(
            font_family = "Merriweather",
            legend = dict(
                title = None, 
                orientation = "h", 
                y = 1, 
                yanchor = "bottom", 
                x = 0.5, 
                xanchor = "center"
            ),
            yaxis_title="Velocidad"
        )
    plotly_url = plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

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

def generate_rose_diagram(DIRECTIONS, data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

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
            font_family = "Merriweather",
            legend = dict(
                title = None, 
                orientation = "h", 
                y = 1, 
                yanchor = "bottom", 
                x = 0.5, 
                xanchor = "center"
            )
        )
    plotly_url = plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_map_graph(geo_data, data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

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
        font_family = "Merriweather"
    )
    plotly_url = plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'