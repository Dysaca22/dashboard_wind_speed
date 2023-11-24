from plotly.express import bar, bar_polar, choropleth_mapbox
from plotly.express.colors import sequential
from pandas import DataFrame
from django.conf import settings
from plotly.offline import plot
import json, os

from wind_speed import vars


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
        barmode = 'group',
        color_discrete_map={
            'MEDIA': '#D593C3',
            'MEDIANA': '#A37FCC'
        }
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
        yaxis_title="VELOCIDAD (m/s)",
        margin=dict(l=5, r=5, b=5, t=10)
    )
    plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_month_speed_graph(data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    df = DataFrame(data)
    df.rename(columns={'month': 'MES', 'avgSpeed': 'MEDIA', 'medSpeed': 'MEDIANA'}, inplace=True)
    fig = bar(
        df, 
        x='MES', 
        y=['MEDIA', 'MEDIANA'], 
        barmode = 'group',
        color_discrete_map={
            'MEDIA': '#D593C3',
            'MEDIANA': '#A37FCC'
        }
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
            yaxis_title="VELOCIDAD (m/s)",
            margin=dict(l=5, r=5, b=5, t=10)
        )
    plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_rose_diagram(DIRECTIONS, data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    data = [*map(lambda x: {'name': x['name'], 'medianSpeed': x['medianSpeed'], 'medianDirection': DIRECTIONS[(int((x['medianDirection']/22.5) + .5) % 16)]}, data)]
    data += [{'name': '', 'medianSpeed': 0, 'medianDirection': d} for d in DIRECTIONS]
    data = [tuple for x in DIRECTIONS for tuple in data if tuple['medianDirection'] == x]
    df = DataFrame(data)
    df.rename(columns={'name': 'Nombre', 'medianSpeed': 'Velocidad (m/s)', 'medianDirection': 'Dirección'}, inplace=True)        
    fig = bar_polar(
        df, 
        r='Velocidad (m/s)', 
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
    plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_rose_month_diagram(DIRECTIONS, data, name):
    path = f'{settings.GRAPHS}/{name}.html'
    if os.path.exists(path):
        return f'graphs/{name}.html'

    data = [*map(lambda x: {'id': f"{x['name']} - {x['month']}", 'medianSpeed': x['medianSpeed'], 'medianDirection': DIRECTIONS[(int((x['medianDirection']/22.5) + .5) % 16)]}, data)]
    data += [{'id': '', 'medianSpeed': 0, 'medianDirection': d} for d in DIRECTIONS]
    data = [tuple for x in DIRECTIONS for tuple in data if tuple['medianDirection'] == x]
    df = DataFrame(data)
    df.rename(columns={'medianSpeed': 'Velocidad (m/s)', 'medianDirection': 'Dirección'}, inplace=True)        
    fig = bar_polar(
        df, 
        r='Velocidad (m/s)', 
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
                orientation = "v",
                traceorder='normal'
            ),
            margin=dict(l=20, r=20, b=20, t=20)
        )
    plot(fig, filename=path, auto_open=False)
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
        labels = {'medianSpeed': 'VELOCIDAD (m/s)'}
    )
    fig.update_layout(
        font = dict(
            family = "Merriweather",
            size = 15
        ),
        margin=dict(l=5, r=5, b=5, t=10)
    )
    plot(fig, filename=path, auto_open=False)
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
            'MEDIANA': '#A37FCC'
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
        yaxis_title="VELOCIDAD (m/s)",
        margin=dict(l=5, r=5, b=5, t=10)
    )
    plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}.html'

def generate_month_map_graph(geo_data, data, name):
    for month in [*vars.MONTH.values()]:
        path = f'{settings.GRAPHS}/{name}{month}.html'
        if os.path.exists(path):
            return f'graphs/{name}'

        geo_json = df_to_geojson(geo_data)
        df = DataFrame(data)
        df.where(df['month'] == month, inplace=True)
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
            labels = {'medianSpeed': 'VELOCIDAD (m/s)'}
        )
        fig.update_layout(
            font = dict(
                family = "Merriweather",
                size = 15
            ),
            margin=dict(l=5, r=5, b=5, t=10)
        )
        plot(fig, filename=path, auto_open=False)
    return f'graphs/{name}'