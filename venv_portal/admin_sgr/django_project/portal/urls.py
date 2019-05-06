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
    # path('portal/equipo', PortalEquipoListView.as_view(), name='equipo'),
    path('portal/equipo_form', views.equipo_form, name='equipo_form'),
    path('portal/pdf', GeneratePDF.as_view(), name='pdf'),

    path('portal/', views.index, name='equipo'),
    path('portal/getdetails/', views.getdetails, name='getdetails'),
    #path(r'^equipo/(?P<equipo_id>\w+)/option', views.getdetails, name='getdetails'),
    #path('portal/', views.person_form, name='person_form'),
    path('add/', views.PersonCreateView.as_view(), name='person_add'),
    path('<int:pk>/', views.PersonUpdateView.as_view(), name='person_change'),

    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]  
