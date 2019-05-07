from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import (
	ListView, 
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
	View
)
from .models import SubComponente, Company, Componente, Tipo, Equipo, Person, City, Country
from dal import autocomplete
from django.utils import timezone
from django.urls import reverse_lazy
from .forms import EquipoForm, PersonForm
import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from portal.utils import render_to_pdf
from django.template.loader import get_template
import json
from django_group_by import GroupByMixin


class RequireLoginMiddleware(object):
    """
    Middleware component that wraps the login_required decorator around
    matching URL patterns. To use, add the class to MIDDLEWARE_CLASSES and
    define LOGIN_REQUIRED_URLS and LOGIN_REQUIRED_URLS_EXCEPTIONS in your
    settings.py. For example:
    ------
    LOGIN_REQUIRED_URLS = (
        r'/topsecret/(.*)$',
    )
    LOGIN_REQUIRED_URLS_EXCEPTIONS = (
        r'/topsecret/login(.*)$',
        r'/topsecret/logout(.*)$',
    )
    ------
    LOGIN_REQUIRED_URLS is where you define URL patterns; each pattern must
    be a valid regex.

    LOGIN_REQUIRED_URLS_EXCEPTIONS is, conversely, where you explicitly
    define any exceptions (like login and logout URLs).
    """

@login_required
# def lista(request):
# 	context = {
# 		'data': SubComponente.objects.all()
# 	}
# 	return render(request, 'portal/subcomponent_list.html', context)
def index(request):
    equipo = Equipo.objects.all()
    print(equipo)
    return render(request, 'portal/person_list.html', {'equipo': equipo})

def getdetails(request):
	if request.method == 'GET':
		equipo_id = request.GET.get('cnt')
		print ('Equipo ID %s' % equipo_id)

		result_set = []
		answer = str(equipo_id[1:-1])
		selected_equipo = Equipo.objects.get(id=answer)
		print('selected %s' % selected_equipo)
		all_componente = selected_equipo.componente_set.all()
		for componente in all_componente:
			print('Componente %s' % componente.nombre)
			result_set.append({'nombre': componente.nombre})
		print('Componente(s) %s' % result_set[0])
		return HttpResponse(json.dumps(result_set), content_type='application/json')

def getdetailsSub(request):
	if request.method == 'GET':
		componente_id = request.GET.get('cnc')
		print ('Componente ID %s' % componente_id)

		result_set = []
		answer = str(componente_id[1:-1])
		selected_componente = Componente.objects.get(nombre=answer)
		# selected_componente = Componente.objects.value_list(nombre=answer, flat=True).distinct()

		print('selected %s' % selected_componente)
		all_subcomponente = selected_componente.subcomponente_set.all()
		for subcomponente in all_subcomponente:
			print('SubComponente %s' % subcomponente.nombre)
			result_set.append({'nombre': subcomponente.nombre})
		print('SubComponente(s) %s' % result_set[0])
		return HttpResponse(json.dumps(result_set), content_type='application/json')

def getdetailsFall(request):
	if request.method == 'GET':
		subcomponente_id = request.GET.get('cnf')
		print ('Componente ID %s' % subcomponente_id)

		result_set = []
		answer = str(subcomponente_id[1:-1])
		selected_subcomponente = SubComponente.objects.get(nombre=answer)
		# selected_componente = Componente.objects.value_list(nombre=answer, flat=True).distinct()

		print('selected %s' % selected_subcomponente)
		all_modofallas = selected_subcomponente.modo_falla_set.all()
		for modofalla in all_modofallas:
			print('Modo Fallas %s' % modofalla.nombre)
			result_set.append({'nombre': modofalla.nombre})
		print('ModoFalla(s) %s' % result_set[0])
		return HttpResponse(json.dumps(result_set), content_type='application/json')

# def getdetailsfallas(request):
# 	if request.method == 'GET':
# 		componente_id = request.GET.get('cnc')
# 		print ('Componente ID %s' % componente_id)
#
# 		result_set = []
# 		answer = str(componente_id[1:-1])
# 		selected_componente = Componente.objects.get(id=answer)
# 		print('selected %s' % selected_equipo)
# 		all_componente = selected_equipo.componente_set.all()
# 		for componente in all_componente:
# 			print('Componente %s' % componente.nombre)
# 			result_set.append({'nombre': componente.nombre})
# 		print('Componente(s) %s' % result_set[0])
# 		return HttpResponse(json.dumps(result_set), content_type='application/json')

def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'portal/hr/city_dropdown_list_options.html', {'cities': cities})

class PortalSubComponenteView(LoginRequiredMixin, ListView):
	 model = SubComponente
	 template_name = 'portal/subcomponent_list.html'
	 context_object_name = 'subcomponente'

	 #comp_objs = Componente.objects.all().prefetch_related('subcomponente_set')

class PortalComponenteView(LoginRequiredMixin, ListView):
	 model = Componente
	 template_name = 'portal/subcomponent_list.html'
	 context_object_name = 'componente'

	 #comp_objs = Componente.objects.all().prefetch_related('subcomponente_set')

class PortalCompanyView(LoginRequiredMixin, ListView):
	 model = Company
	 template_name = 'portal/company_list.html'
	 context_object_name = 'compania'

class PortalTipoView(LoginRequiredMixin, ListView):
	 model = Tipo
	 context_object_name = 'tipo'

class PortalEquipoListView(LoginRequiredMixin, ListView):
	 model = Equipo
	 template_name = 'portal/'
	 context_object_name = 'equipo'

def equipo_form(request):
	#form = EquipoForm(request.Equipo or None, initial={'Affiliazione': initial_value})
	form = EquipoForm()
	return render(request, 'portal/equipo_form.html', {'form':form})

class GeneratePDF(View):
	def get(self, request, *args, **kwargs):
		template = get_template('portal/pdf/invoice.html')
		context = {
			 "invoice_id": 133,
			 "inspector_name": "John Doe",
			 "equipo": "PALA ELECTRICA PE0001",
			 "tipo_inspeccion": "VISUAL",
			 "fecha": "25 / 04 / 2019",
			 "componente": "Perforadora PF0005",
			 "cliente": "MINERA LOS PELAMBRES",
		}
		html = template.render(context) 
		pdf = render_to_pdf('portal/pdf/invoice.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Report_%s.pdf" %("12341231")
			content = "inline; filename='%s'" %(filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" %(filename)
			response['Content-Disposition'] = content
			return response
		return HttpResponse("Not Found")

# class PersonListView(ListView):
# 	 def person_form(request):
# 	form = PersonForm()
#  	return render(request, 'portal/person_list.html', {'form':form})

class PersonCreateView(CreateView):
    model = Person
    success_url = reverse_lazy('person_changelist')

class PersonUpdateView(UpdateView):
    model = Person
    success_url = reverse_lazy('person_changelist')

# def load_cities(request):
#     country_id = request.GET.get('country')
#     cities = City.objects.filter(country_id=country_id).order_by('name')
#     return render(request, 'portal/hr/city_dropdown_list_options.html', {'cities': cities})
#


# def create_user(request):
# 	#if request.method == 'POST':
# 	name = request.POST['name']
# 	email = request.POST['email']
# 	password = request.POST['password']
#
# 	User.objects.create(
# 		name=name,
# 		email=email,
# 		password=password
# 	)
#
# 	return HttpResponse('')


# class ComponenteAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         # Don't forget to filter out results depending on the visitor !
#         if not self.request.user.is_authenticated():
#             return Componente.objects.none()
#
#         qs = Componente.objects.all()
#
#         if self.q:
#             qs = qs.filter(name__istartswith=self.q)
#
#         return qs
