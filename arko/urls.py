from django.urls import path
from .views import StateListView, CompanyListView, DistrictListView, MunicipalityListView, logout_view

app_name = 'arko'

urlpatterns = [
    path('states/', StateListView.as_view(), name='state-list'),
    path('municipalities/', MunicipalityListView.as_view(), name='municipality-list'),
    path('districts/', DistrictListView.as_view(), name='district-list'),
    path('companies/', CompanyListView.as_view(), name='company-list'),
    path('logout/', logout_view, name='logout-custom')
]