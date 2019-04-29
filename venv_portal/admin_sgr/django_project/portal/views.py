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
from .models import SubComponente, Company, Componente, Tipo, Equipo
from django.utils import timezone
from django.urls import reverse_lazy
from .forms import EquipoForm
import re
from django.conf import settings
from django.contrib.auth.decorators import login_required
from portal.utils import render_to_pdf
from django.template.loader import get_template

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
def lista(request):
	context = {
		'data': SubComponente.objects.all()
	}
	return render(request, 'portal/subcomponent_list.html', context)

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
	 template_name = 'portal/equipo_list.html'
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

		
	 