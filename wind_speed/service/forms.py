from django import forms


class LocationForm(forms.Form):
    LocationsEnum = (
        ("Departamento", "Departamento"),
        ("Municipio", "Municipio"),
        ("Region", "Región"),
    )

    location = forms.ChoiceField(
        label = "Selecciona tu localidad",
        choices = LocationsEnum
    )

    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.initial['location'] = 0