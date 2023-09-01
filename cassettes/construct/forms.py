from django import forms
from cassettes.construct.models import Cassette,CassetteAssembly,Workstation,Modulemap,Step, CassetteType


class PlacePart(forms.ModelForm):
    class Meta:
        model = CassetteAssembly
        fields = ('barcode','placed')

class CassetteForm(forms.ModelForm):
    side = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Cassette
        fields = ('name','workstation','barcode')
        widgets = {
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.Select(attrs={'class': 'form-control'}),
            'workstation': forms.Select(attrs={'class': 'form-control'})
        }

class CassetteAssemblyForm(forms.ModelForm):
    cassette_barcode = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cassette_name = forms.ModelChoiceField(queryset=CassetteType.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    cassette_workstation = forms.ModelChoiceField(queryset=Workstation.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = CassetteAssembly
        fields = ('cassette_barcode','cassette_name', 'cassette_workstation', 'side')
        widgets = {
            'cassette_barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'cassette_name': forms.Select(attrs={'class': 'form-control'}),
            'cassette_workstation': forms.Select(attrs={'class': 'form-control'}),
            'side': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def save(self, commit=True):
        cassette_barcode = self.cleaned_data['cassette_barcode']
        cassette_name = self.cleaned_data['cassette_name']
        cassette_workstation = self.cleaned_data['cassette_workstation']
        cassette, _ = Cassette.objects.get_or_create(barcode=cassette_barcode, name=cassette_name, workstation=Workstation.objects.get(name=cassette_workstation))
        cassette_assembly = super().save(commit=False)
        # cassette_assembly.cassette = cassette
        selectedworkstation = Workstation.objects.get(name=cassette_workstation)
        selectedworkstation.cassette = cassette
        selectedworkstation.save()
        #if commit:
            # cassette_assembly.save()
        return cassette_assembly

class WorkstationForm(forms.ModelForm):
    class Meta:
        model = Workstation
        fields = "__all__"

class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = "__all__"