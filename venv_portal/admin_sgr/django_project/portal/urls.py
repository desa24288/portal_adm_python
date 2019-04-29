from django.urls import include, path
from .views import (
	PortalSubComponenteView,
    PortalComponenteView,
    PortalCompanyView,
    PortalEquipoListView,
    GeneratePDF,
)
from . import views

urlpatterns = [
    path('portal/subcomponente', PortalSubComponenteView.as_view(), name='subcomponente'),
    path('portal/company', PortalCompanyView.as_view(), name='company'),
    path('portal/equipo', PortalEquipoListView.as_view(), name='equipo'),
    path('portal/equipo_form', views.equipo_form, name='equipo_form'),
    path('portal/pdf', GeneratePDF.as_view(), name='pdf'),
]  