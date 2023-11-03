from django.views.generic import TemplateView
from django.urls import reverse
import plotly.express as px
import pandas as pd

from data.schema import schema
from .utils import read_json
from .forms import LocationForm


class GeneralDataView(TemplateView):
    template_name = 'service/home.html'

    def get_context_data(self, **kwargs):
        query = """
            {
                generalData{
                    noStates
                    noDepartments
                    noRecords
                }
            }
        """

        result_ = schema.execute(query).data['generalData'][0]
        kwargs.update({
            'noStates': result_['noStates'],
            'noDepartments': result_['noDepartments'],
            'noRecords': result_['noRecords']
        })
        return super().get_context_data(**kwargs)


class LocationDataView(TemplateView):
    template_name = 'service/location_data.html'
    DIRECTIONS = ["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]

    def generate_rose_diagram(self, data):
        data = [*map(lambda x: {'name': x['name'], 'medianSpeed': x['medianSpeed'], 'medianDirection': self.DIRECTIONS[(int((x['medianDirection']/22.5) + .5) % 16)]}, data)]
        data += [{'name': '', 'medianSpeed': 0, 'medianDirection': d} for d in self.DIRECTIONS]
        data = [tuple for x in self.DIRECTIONS for tuple in data if tuple['medianDirection'] == x]
        df = pd.DataFrame(data)
        df.rename(columns={'name': 'Nombre', 'medianSpeed': 'Velocidad', 'medianDirection': 'Dirección'}, inplace=True)        
        fig = px.bar_polar(df, r='Velocidad', theta='Dirección', color='Nombre', color_discrete_sequence=px.colors.sequential.Plasma_r)
        return fig.to_html()

    def generate_map_graph(self, location, data):
        urls = {
            'Departamento': 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json',
            'Municipio': 'https://gist.githubusercontent.com/john-guerra/727e8992e9599b9d9f1dbfdc4c8e479e/raw/090f8b935a437e24d65b64d87598fbb437c006da/colombia-municipios.json',
            'Region': 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
        }
        ids = {
            'Departamento': 'NOMBRE_DPT',
            'Municipio': 'name',
            'Region': 'NOMBRE_DPT'
        }
        json_departments_colombia = read_json(urls[location])
        [*filter(lambda x: 'BOGOTA' in x['properties'][ids[location]], json_departments_colombia['features'])][0]['properties'][ids[location]] = 'BOGOTA'
        [*filter(lambda x: 'NARIÑO' in x['properties'][ids[location]], json_departments_colombia['features'])][0]['properties'][ids[location]] = 'NARINO'
        df = pd.DataFrame(data)
        df['name'] = df['name'].str.upper()
        df.rename(columns={'name': 'Nombre'}, inplace=True)
        fig = px.choropleth_mapbox(
            df, 
            geojson = json_departments_colombia, 
            locations = 'Nombre',
            featureidkey = f'properties.{ids[location]}',
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


    def get_context_data(self, location, **kwargs):
        query = """
            {{
                locationData(location: "{}"){{
                    name
                    medianSpeed
                    medianDirection
                }}
            }}
        """.format(location)
        result_ = schema.execute(query).data['locationData']
        rose_diagram = self.generate_rose_diagram(result_)
        map_diagram_speed = self.generate_map_graph(location, result_)

        kwargs.update({
            'rose_graph': rose_diagram,
            'map_graph': map_diagram_speed,
        })
        return super().get_context_data(**kwargs)

    def get(self, request, **kwargs):
        form = LocationForm()
        context = self.get_context_data("Departamento", **kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, **kwargs):
        form = LocationForm(request.POST)
        context = self.get_context_data("Departamento", **kwargs)
        context['form'] = form
        if form.is_valid():
            location = form.cleaned_data["location"]
            context = self.get_context_data(location, **kwargs)
            context['form'] = form
            return self.render_to_response(context)
        return self.render_to_response(context)