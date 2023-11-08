from django.views.generic import TemplateView
from django.urls import reverse

from data.schema import schema
from .utils import generate_rose_diagram, generate_map_graph, generate_date_speed_graph
from .forms import LocationForm


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
                allWind{
                    date
                    speed
                }
            }
        """
        allWindResult_ = schema.execute(query).data['allWind']
        generate_date_speed_graph(allWindResult_)
        
        kwargs.update({
            'noStates': result_['noStates'],
            'noDepartments': result_['noDepartments'],
            'noRegions': result_['noRegions'],
            'noStations': result_['noStations'],
            'noRecords': result_['noRecords']
        })
        return super().get_context_data(**kwargs)


class LocationDataView(TemplateView):
    template_name = 'service/location_data.html'
    DIRECTIONS = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]

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

        rose_diagram = generate_rose_diagram(self.DIRECTIONS, result_)
        map_diagram_speed = generate_map_graph(geoResult_, result_)

        kwargs.update({
            'rose_graph': rose_diagram,
            'map_graph': map_diagram_speed,
        })
        return super().get_context_data(**kwargs)

    def get(self, request, **kwargs):
        if 'location' in request.GET:
            form = LocationForm(request.GET)
            if form.is_valid():
                location = form.cleaned_data["location"]
                context = self.get_context_data(location, **kwargs)
                context['form'] = form
                return self.render_to_response(context)                
        form = LocationForm()
        context = self.get_context_data("department", **kwargs)
        context['form'] = form
        return self.render_to_response(context)