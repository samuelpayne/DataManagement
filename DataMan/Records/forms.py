from django import forms
from django.core.exceptions import ValidationError

class AddSampleForm(forms.Form):
    name = forms.CharField(help_text ="Sample Name")
    ID = forms.IntegerField(help_text ="Sample ID")
    experiment = forms.IntegerField(help_text="Experiment ID")
    """dataset
    preceeding_sample
    storage_condition
    location
    container
    treatment_protocal
    created
    organism
    modifications"""

    def check_name(self):
        valname = self.cleaned_data['name']

        #replace with checking for pre-existing names
        if name=="ERROR-FAIL-FAIL-ERROR-FAIL":
            raise ValidationError('You had one job.')

        return valname
