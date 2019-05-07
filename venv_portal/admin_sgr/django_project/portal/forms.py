from django import forms
# from dal import
#from django_select2.forms import ModelSelect2Widget
from .models import Equipo, Componente, Company, Person, City, SubComponente, Modo_Falla
from django.http import HttpResponse
import json


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('name', 'birthdate', 'country', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

class EquipoForm(forms.ModelForm):

	def form_valid(self, form):
	 	form.instance.author = self.request.user
	 	return super().form_valid(form)
	class Meta:
		model = Equipo
		fields = ('nombre','descripcion')

	#Descripcion = forms.CharField(widget=forms.Textarea)
	Cliente = forms.ModelChoiceField(queryset=Company.objects.all())
	Equipo = forms.ModelChoiceField(queryset=Equipo.objects.all())
	Componente = forms.ModelChoiceField(queryset=Componente.objects.all())
	SubComponente = forms.ModelChoiceField(queryset=SubComponente.objects.all())
	Modo_Falla = forms.ModelChoiceField(queryset=Modo_Falla.objects.all())

def getdetails(request):
	if request.method == 'GET':
		equipo_id = request.GET.get('cnt')
		print ('Equipo ID %s' % equipo_id)
		# return HttpResponse(simplejson.dumps(equipo_id))

		result_set = []
		# all_componente = []
		answer = str(equipo_id[1:-1])
		selected_equipo = Equipo.objects.get(id=answer)
		print('selected %s' % selected_equipo)
		all_componente = selected_equipo.componente_set.all()
		for componente in all_componente:
			print('Componente %s' % componente.nombre)
			result_set.append({'nombre': componente.nombre})
		print('Componente(s) %s' % result_set[0])
		return HttpResponse(json.dumps(result_set), content_type='application/json')
	#def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['nombre'].queryset = Componente.objects.none()
    #days = forms.ChoiceField(choices=[(x, x) for x in (1, 32)])
