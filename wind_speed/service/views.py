from django.views.generic import TemplateView
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
        result_ = [*map(lambda x: {'name': x['name'], 'medianSpeed': x['medianSpeed'], 'medianDirection': self.DIRECTIONS[(int((x['medianDirection']/22.5) + .5) % 16)]}, result_)]
        result_ += [{'name': '', 'medianSpeed': 0, 'medianDirection': d} for d in self.DIRECTIONS]
        result_ = [tuple for x in self.DIRECTIONS for tuple in result_ if tuple['medianDirection'] == x]
        df = pd.DataFrame(result_)
        df.rename(columns={'name': 'Nombre', 'medianSpeed': 'Velocidad', 'medianDirection': 'Dirección'}, inplace=True)        
        fig = px.bar_polar(df, r='Velocidad', theta='Dirección', color='Nombre', color_discrete_sequence=px.colors.sequential.Plasma_r)
        fig_html = fig.to_html()

        kwargs.update({
            'graph': fig_html,
        })
        return super().get_context_data(**kwargs)