from django.urls import path
from .views.web import StateListView, CompanyListView, DistrictListView, MunicipalityListView, logout_view
from .views.api import StateAPIListView, MunicipalityAPIListView, DistrictAPIListView, CompanyAPIListView

app_name = 'arko'

urlpatterns = [
    path('states/', StateListView.as_view(), name='state-list'),
    path('municipalities/', MunicipalityListView.as_view(), name='municipality-list'),
    path('districts/', DistrictListView.as_view(), name='district-list'),
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('logout/', logout_view, name='logout-custom'),

    #URLs de API
    path('api/states/', StateAPIListView.as_view(), name='state-api-list'),
    path('api/municipalities/', MunicipalityAPIListView.as_view(), name='municipality-api-list'),
    path('api/districts/', DistrictAPIListView.as_view(), name='district-api-list'),
    path('api/companies/', CompanyAPIListView.as_view(), name='company-api-list'),
]