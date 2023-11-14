from django.views.generic import TemplateView

from data.schema import schema
from .utils import (
    generate_hour_speed_graph, 
    generate_month_speed_graph,
    generate_rose_diagram, 
    generate_map_graph,
    generate_location_speed_graph,
    generate_rose_month_diagram,
    generate_month_map_graph
)
from wind_speed import vars


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
                monthSpeed{
                    month
                    avgSpeed
                    medSpeed
                }
            }
        """
        monthSpeedResult_ = schema.execute(query).data['monthSpeed']
        query = """
            {
                locationData{
                    name
                }
            }
        """
        namesResult_ = schema.execute(query).data['locationData']
        names = [row['name'] for row in namesResult_]
        hour_speed_graph = generate_hour_speed_graph(hourSpeedResult_, 'hour_speed')
        month_speed_graph = generate_month_speed_graph(monthSpeedResult_, 'month_speed')
        
        kwargs.update({
            'names': names,
            'noStates': result_['noStates'],
            'noDepartments': result_['noDepartments'],
            'noRegions': result_['noRegions'],
            'noStations': result_['noStations'],
            'noRecords': result_['noRecords'],
            'hour_speed_url': hour_speed_graph,
            'month_speed_url': month_speed_graph,
        })
        return super().get_context_data(**kwargs)


class LocationDataView(TemplateView):
    template_name = 'service/location_data.html'

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
        rose_diagram = generate_rose_diagram(vars.DIRECTIONS, result_, f'rose_direction_{location}')
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
            'name': vars.LOCATION[location]
        })
        return super().get_context_data(**kwargs)


class LocationMonthDataView(TemplateView):
    template_name = 'service/location_month_data.html'

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
            row['month'],
            round(float(row['avgSpeed']), 2), 
            round(float(row['medianSpeed']), 2),
            round(float(row['devSpeed']), 2),
            round(float(row['avgDirection']), 2),
            round(float(row['medianDirection']), 2),
            round(float(row['devDirection']), 2)
            ] for row in result_
        ]
        names = [row['name'] for row in result_]
        rose_month_diagram = generate_rose_month_diagram(vars.DIRECTIONS, result_, f'rose_month_direction_{location}')
        map_diagram_speed = generate_month_map_graph(geoResult_, result_, f'colombian_map_{location}_')
        table_min_max = [[row['name'], row['month'], round(float(row['minSpeed']), 2), round(float(row['maxSpeed']), 2)] for row in result_]

        kwargs.update({
            'names': names,
            'months': [*vars.MONTH.values()],
            'table_data': table_data,
            'rose_graph_url': rose_month_diagram,
            'map_graph_url': map_diagram_speed,
            'table_min_max': table_min_max,
            'name': vars.LOCATION[location]
        })
        return super().get_context_data(**kwargs)