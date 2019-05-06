from django import forms
# from dal import
#from django_select2.forms import ModelSelect2Widget
from .models import Equipo, Componente, Company, Person, City, SubComponente, Modo_Falla

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

	#def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['nombre'].queryset = Componente.objects.none()
    #days = forms.ChoiceField(choices=[(x, x) for x in (1, 32)])
