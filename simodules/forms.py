from django import forms

class NewPCB(forms.Form):
    pcb_id = forms.IntegerField(required=True)
    title = forms.CharField(max_length=50)