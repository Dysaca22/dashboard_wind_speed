from plotly.express import bar, bar_polar, choropleth_mapbox
from plotly.express.colors import sequential
from pandas import DataFrame, to_datetime, concat
from django.conf import settings
from plotly.offline import plot
import json, os


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
        if 'san andres' in element['name']:
                feature['properties']['name'] = 'San andres'
        elif 'bogota' in element['name']:
            feature['properties']['name'] = 'Bogota d.c'
        else:
            feature['properties']['name'] = element['name']
        feature['properties']['area'] = element['area']
        feature['properties']['perimeter'] = element['perimeter']
        feature['properties']['hectares'] = element['hectares']
        geojson['features'].append(feature)
    return geojson

def generate_hour_speed_graph(data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    df = DataFrame(data)
    df.rename(columns={'hour': 'HORA', 'avgSpeed': 'MEDIA', 'medSpeed': 'MEDIANA'}, inplace=True)
    fig = bar(
        df, 
        x='HORA', 
        y=['MEDIA', 'MEDIANA'], 
        barmode = 'group'
    )
    fig.update_layout(
            font = dict(
                family = "Merriweather",
                size = 15
            ),
            legend = dict(
                title = None, 
                orientation = "h", 
                y = 1, 
                yanchor = "bottom", 
                x = 0.5, 
                xanchor = "center"
            ),
            yaxis_title="VELOCIDAD",
            margin=dict(l=5, r=5, b=5, t=10)
        )
    plotly_url = plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_rose_diagram(DIRECTIONS, location, data, name):
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
            font = dict(
                family = "Merriweather",
                size = 15
            ),
            legend = dict(
                title = None,
                orientation = "v"
            ),
            margin=dict(l=20, r=20, b=20, t=20)
        )
    plotly_url = plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_rose_month_diagram(DIRECTIONS, MONTH, location, data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    data = [*map(lambda x: {'name': x['name'], 'month': MONTH[x['month']], 'medianSpeed': x['medianSpeed'], 'medianDirection': DIRECTIONS[(int((x['medianDirection']/22.5) + .5) % 16)]}, data)]
    data += [{'name': '', 'month': '', 'medianSpeed': 0, 'medianDirection': d} for d in DIRECTIONS]
    data = [tuple for x in DIRECTIONS for tuple in data if tuple['medianDirection'] == x]
    df = DataFrame(data)
    df.rename(columns={'name': 'Nombre', 'medianSpeed': 'Velocidad', 'medianDirection': 'Dirección', 'month': 'Mes'}, inplace=True)        
    df['id'] = df['Nombre'] + ' - ' + df['Mes']
    df = df.sort_values(by='id')
    fig = bar_polar(
        df, 
        r='Velocidad', 
        theta='Dirección', 
        color='id', 
        color_discrete_sequence=sequential.Plasma_r
    )
    fig.update_layout(
            font = dict(
                family = "Merriweather",
                size = 15
            ),
            legend = dict(
                title = None,
                orientation = "v"
            ),
            margin=dict(l=20, r=20, b=20, t=20)
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
        color_continuous_scale='Plasma',
        range_color = (df['medianSpeed'].min(), df['medianSpeed'].max()),
        mapbox_style = "carto-positron",
        zoom = 4.4,
        center = {"lat": 4.0, "lon": -73.0},
        opacity=  0.5,
        labels = {'medianSpeed': 'VELOCIDAD'}
    )
    fig.update_layout(
        font = dict(
            family = "Merriweather",
            size = 15
        ),
        margin=dict(l=5, r=5, b=5, t=10)
    )
    plotly_url = plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_location_speed_graph(data, location, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    df = DataFrame(data)
    df.rename(columns={'name': location.upper(), 'avgSpeed': 'MEDIA', 'medianSpeed': 'MEDIANA'}, inplace=True)
    fig = bar(
        df, 
        x=location.upper(), 
        y=['MEDIA', 'MEDIANA'], 
        barmode = 'group',
        color_discrete_map={
            'MEDIA': '#D593C3',
            'MEDIANA': '#A37FCC',
        }
    )
    fig.update_layout(
        font = dict(
            family = "Merriweather",
            size = 15
        ),
        xaxis = dict(
            tickangle = 45,
            title = None
        ),
        legend = dict(
            title = None, 
            orientation = "h", 
            y = 1, 
            yanchor = "bottom", 
            x = 0.5, 
            xanchor = "center"
        ),
        yaxis_title="VELOCIDAD",
        margin=dict(l=5, r=5, b=5, t=10)
    )
    plotly_url = plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'