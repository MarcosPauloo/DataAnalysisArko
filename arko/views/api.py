from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

# Importando nossos models, serializers e filters
from ..models import State, Municipality, District, Company
from ..serializers import StateSerializer, MunicipalitySerializer, DistrictSerializer, CompanySerializer
from ..filters import StateFilter, MunicipalityFilter, DistrictFilter, CompanyFilter

class StandardResultSetPagination(PageNumberPagination):
    """"
    Define um padrão de paginação para a API, com 25 resultados por página.
    """
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100


# --- ENDPOINTS ---

class StateAPIListView(ListAPIView):
    """"
    API endpoint que retorna uma lista paginada e filtrável de Estados.
    """
    # select_related para evitar queries extras
    queryset = State.objects.select_related('regiao').all()

    serializer_class = StateSerializer
    pagination_class = StandardResultSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = StateFilter

class MunicipalityAPIListView(ListAPIView):
    """"
    API endpoint que retorna uma lista paginada e filtrável de Municípios.
    """
    queryset = Municipality.objects.select_related('estado').all()
    serializer_class = MunicipalitySerializer
    pagination_class = StandardResultSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MunicipalityFilter

class DistrictAPIListView(ListAPIView):
    """
    API endpoint que retorna uma lista paginada e filtrável de Distritos.
    """
    queryset = District.objects.select_related('municipio__estado').all()
    serializer_class = DistrictSerializer
    pagination_class = StandardResultSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = DistrictFilter

class CompanyAPIListView(ListAPIView):
    """"
    API endpoing que retorna uma lista paginada e filtrável de Empresas.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = StandardResultSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CompanyFilter