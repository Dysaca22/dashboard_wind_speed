from django.views.generic import TemplateView
from windrose import WindroseAxes
import plotly.express as px
import pandas as pd

from data.schema import schema


class GeneralDataView(TemplateView):
    template_name = 'service/general_data.html'

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

    def get_context_data(self, **kwargs):
        query = """
            {
                locationData(location: "Departamento"){
                    name
                    medianSpeed
                    medianDirection
                }
            }
        """
        result_ = schema.execute(query).data['locationData']

        df = pd.DataFrame(result_)        
        df['medianDirection'] = [*map(lambda x: self.DIRECTIONS[(int((x/22.5) + .5) % 16)], df['medianDirection'])]
        print(df)
        fig = px.bar_polar(df, r="medianSpeed", theta="medianDirection", template="plotly_dark", color_discrete_sequence= px.colors.sequential.Plasma_r)
        fig_html = fig.to_html()

        kwargs.update({
            'graph': fig_html,
        })
        return super().get_context_data(**kwargs)