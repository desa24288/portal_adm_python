from django import forms
from .models import Equipo, Componente, Company

class EquipoForm(forms.ModelForm):
	class Meta:
		model = Equipo
		fields = ('nombre','descripcion')

	#Descripcion = forms.CharField(widget=forms.Textarea)
	Cliente = forms.ModelChoiceField(queryset=Company.objects.all())
	Equipo = forms.ModelChoiceField(queryset=Equipo.objects.all())
	Componente = forms.ModelChoiceField(queryset=Componente.objects.all())
	#def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['nombre'].queryset = Componente.objects.none()
    #days = forms.ChoiceField(choices=[(x, x) for x in (1, 32)])