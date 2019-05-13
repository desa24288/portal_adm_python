from django.urls import include, path
from .views import (
    IndexView,
	PortalSubComponenteView,
    PortalComponenteView,
    PortalCompanyView,
    PortalEquipoListView,
    GeneratePDF
)
from . import views

urlpatterns = [
    path('portal/subcomponente', PortalSubComponenteView.as_view(), name='subcomponente'),
    path('portal/company', PortalCompanyView.as_view(), name='company'),
    path('portal/equipo_form', views.equipo_form, name='equipo_form'),
    path('portal/pdf', GeneratePDF.as_view(), name='pdf'),
    path('portal/', IndexView.as_view(), name='home_list'),
    path('portal/getdetails/', views.getdetails, name='getdetails'),
    path('portal/getdetailsSub/', views.getdetailsSub, name='getdetailsSub'),
    path('portal/getdetailsFall/', views.getdetailsFall, name='getdetailsFall'),
    path('add/', views.PersonCreateView.as_view(), name='person_add'),
    path('<int:pk>/', views.PersonUpdateView.as_view(), name='person_change'),

    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
]  
