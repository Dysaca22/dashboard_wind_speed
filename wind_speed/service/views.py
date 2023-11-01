from django.views.generic import TemplateView
from django.shortcuts import render

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

    def get_context_data(self, **kwargs):
        query = """
            {
                locationData(location="Departamento"){
                    name
                    medianSpeed
                    medianDirection
                }
            }
        """

        result_ = schema.execute(query).data['locationData']
        names, speeds, directions = [*zip(*result_)]
        kwargs.update({
            'noStates': result_['noStates'],
            'noDepartments': result_['noDepartments'],
            'noRecords': result_['noRecords']
        })
        return super().get_context_data(**kwargs)