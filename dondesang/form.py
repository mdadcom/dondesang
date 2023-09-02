from django import forms 
from .models import *

class PaysForm(forms.ModelForm):
    class Meta:
        model = Pays
        fields='__all__'
        Widgets={
            'nom':forms.TextInput(attrs={'class': 'form-control'}),
            'code':forms.TextInput(attrs={'class': 'form-control'}),
        }

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields='__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom'].widget.attrs.update({'class':'form-control'})

class VilleForm(forms.ModelForm):
    class Meta:
        model = Ville
        fields='__all__'
        
class CollectsForm(forms.ModelForm):
    class Meta:
        model = Collects
        fields='__all__'
        Widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'ville': forms.Select(attrs={'class': 'form-control'}),
            'date':forms.DateInput(attrs={'class': 'form-control'}),
        }
        
class DonneurForm(forms.ModelForm):
    class Meta:
        model = Donneur
        fields='__all__'

class EntretienForm(forms.ModelForm):
    class Meta:
        model = Entretien
        fields='__all__'