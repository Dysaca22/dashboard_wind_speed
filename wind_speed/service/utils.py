from plotly.express import bar_polar, choropleth_mapbox
from plotly.express.colors import sequential
from pandas import DataFrame
import json


def df_to_geojson(df):
    df = DataFrame(df)
    geojson = {'type': 'FeatureCollection', 'features': []}

    for i, element in df.iterrows():
        feature = {'type': 'Feature', 
                   'properties': {}}
        
        feature['geometry'] = json.loads(json.loads(element['geometry']))
        if 'Nariño' in element['name']:
                feature['properties']['name'] = 'Narino'
        elif 'bogota' in element['name']:
            feature['properties']['name'] = 'Bogota d.c'
        else:
            feature['properties']['name'] = element['name']
        #feature['properties']['area'] = element['area']
        #feature['properties']['perimeter'] = element['perimeter']
        #feature['properties']['hectares'] = element['hectares']
        geojson['features'].append(feature)
    
    return geojson

def generate_rose_diagram(DIRECTIONS, data):
    data = [*map(lambda x: {'name': x['name'], 'medianSpeed': x['medianSpeed'], 'medianDirection': DIRECTIONS[(int((x['medianDirection']/22.5) + .5) % 16)]}, data)]
    data += [{'name': '', 'medianSpeed': 0, 'medianDirection': d} for d in DIRECTIONS]
    data = [tuple for x in DIRECTIONS for tuple in data if tuple['medianDirection'] == x]
    df = DataFrame(data)
    df.rename(columns={'name': 'Nombre', 'medianSpeed': 'Velocidad', 'medianDirection': 'Dirección'}, inplace=True)        
    fig = bar_polar(df, r='Velocidad', theta='Dirección', color='Nombre', color_discrete_sequence=sequential.Plasma_r)
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
            mapbox_style = "white-bg",
            zoom = 4,
            center = {"lat": 3.5495372146017536, "lon": -73.04261938707367},
            opacity=  0.5,
            labels = {'medianSpeed': 'Velocidad'}
        )
        return fig.to_html()