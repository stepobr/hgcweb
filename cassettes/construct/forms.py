from django import forms
from cassettes.construct.models import Cassette,Part,Workstation,Modulemap,Step


class PlacePart(forms.ModelForm):
    class Meta:
        model = Part
        fields = ('barcode','placed')

class CassetteForm(forms.ModelForm):
    class Meta:
        model = Cassette
        fields = ('name','workstation','barcode','side')
        widgets = {
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.Select(attrs={'class': 'form-control'}),
            'side': forms.TextInput(attrs={'class': 'form-control'}),
            'workstation': forms.Select(attrs={'class': 'form-control'})
        }

class WorkstationForm(forms.ModelForm):
    class Meta:
        model = Workstation
        fields = "__all__"

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = "__all__"