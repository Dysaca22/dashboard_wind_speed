from django.views.generic import TemplateView
from django.urls import reverse

from data.schema import schema
from .utils import (
    generate_hour_speed_graph, 
    generate_rose_diagram, 
    generate_map_graph,
    generate_location_speed_graph,
    generate_rose_month_diagram
)


class GeneralDataView(TemplateView):
    template_name = 'service/home.html'

    def get_context_data(self, **kwargs):
        query = """
            {
                generalData{
                    noStates
                    noDepartments
                    noRegions
                    noStations
                    noRecords
                }
            }
        """
        result_ = schema.execute(query).data['generalData'][0]
        query = """
            {
                hourSpeed{
                    hour
                    avgSpeed
                    medSpeed
                }
            }
        """
        hourSpeedResult_ = schema.execute(query).data['hourSpeed']
        query = """
            {
                locationData{
                    name
                }
            }
        """
        namesResult_ = schema.execute(query).data['locationData']
        names = [row['name'] for row in namesResult_]
        hour_speed_url = generate_hour_speed_graph(hourSpeedResult_, 'hour_speed')
        
        kwargs.update({
            'names': names,
            'noStates': result_['noStates'],
            'noDepartments': result_['noDepartments'],
            'noRegions': result_['noRegions'],
            'noStations': result_['noStations'],
            'noRecords': result_['noRecords'],
            'hour_speed_url': hour_speed_url
        })
        return super().get_context_data(**kwargs)


class LocationDataView(TemplateView):
    template_name = 'service/location_data.html'
    DIRECTIONS = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    LOCATION = {
        'region': 'Región',
        'department': 'Departamento',
        'state': 'Municipio'
    }

    def get_context_data(self, tipo, **kwargs):
        location=tipo
        query = """
            {{
                locationData(location: "{}"){{
                    name
                    avgSpeed
                    medianSpeed
                    devSpeed
                    minSpeed
                    maxSpeed
                    avgDirection
                    medianDirection
                    devDirection
                }}
            }}
        """.format(location)
        result_ = schema.execute(query).data['locationData']
        query = """
            {{
                geoData(location: "{}"){{
                    name
                    geometry
                    area
                    perimeter
                    hectares
                }}
            }}
        """.format(location)
        geoResult_ = schema.execute(query).data['geoData']

        table_data = [
            [row['name'], 
            round(float(row['avgSpeed']), 2), 
            round(float(row['medianSpeed']), 2),
            round(float(row['devSpeed']), 2),
            round(float(row['avgDirection']), 2),
            round(float(row['medianDirection']), 2),
            round(float(row['devDirection']), 2)
            ] for row in result_
        ]
        names = [row['name'] for row in result_]
        rose_diagram = generate_rose_diagram(self.DIRECTIONS, location, result_, f'rose_direction_{location}')
        map_diagram_speed = generate_map_graph(geoResult_, result_, f'colombian_map_{location}')
        bar_speed_graph = generate_location_speed_graph(result_, location, f'{location}_bar_speed')
        table_min_max = [[row['name'], round(float(row['minSpeed']), 2), round(float(row['maxSpeed']), 2)] for row in result_]

        kwargs.update({
            'names': names,
            'table_data': table_data,
            'rose_graph_url': rose_diagram,
            'map_graph_url': map_diagram_speed,
            'bar_graph_url': bar_speed_graph,
            'table_min_max': table_min_max,
            'name': self.LOCATION[location]
        })
        return super().get_context_data(**kwargs)


class LocationMonthDataView(TemplateView):
    template_name = 'service/location_month_data.html'
    DIRECTIONS = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    LOCATION = {
        'region': 'Región',
        'department': 'Departamento',
        'state': 'Municipio'
    }
    MONTH = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre'
    }

    def get_context_data(self, tipo, **kwargs):
        location=tipo
        query = """
            {{
                locationMonthData(location: "{}"){{
                    name
                    month
                    avgSpeed
                    medianSpeed
                    devSpeed
                    minSpeed
                    maxSpeed
                    avgDirection
                    medianDirection
                    devDirection
                }}
            }}
        """.format(location)
        result_ = schema.execute(query).data['locationMonthData']
        query = """
            {{
                geoData(location: "{}"){{
                    name
                    geometry
                    area
                    perimeter
                    hectares
                }}
            }}
        """.format(location)
        geoResult_ = schema.execute(query).data['geoData']

        table_data = [
            [row['name'], 
            self.MONTH[row['month']],
            round(float(row['avgSpeed']), 2), 
            round(float(row['medianSpeed']), 2),
            round(float(row['devSpeed']), 2),
            round(float(row['avgDirection']), 2),
            round(float(row['medianDirection']), 2),
            round(float(row['devDirection']), 2)
            ] for row in result_
        ]
        names = [row['name'] for row in result_]
        rose_month_diagram = generate_rose_month_diagram(self.DIRECTIONS, self.MONTH, location, result_, f'rose_month_direction_{location}')
        map_diagram_speed = generate_map_graph(geoResult_, result_, f'colombian_map_month_{location}')
        table_min_max = [[row['name'], self.MONTH[row['month']], round(float(row['minSpeed']), 2), round(float(row['maxSpeed']), 2)] for row in result_]

        kwargs.update({
            'names': names,
            'table_data': table_data,
            'rose_graph_url': rose_month_diagram,
            'map_graph_url': map_diagram_speed,
            'table_min_max': table_min_max,
            'name': self.LOCATION[location]
        })
        return super().get_context_data(**kwargs)