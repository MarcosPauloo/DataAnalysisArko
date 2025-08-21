import django_filters
from .models import Company, Municipality, District, Region, State

class CompanyFilter(django_filters.FilterSet):
    razao_social=django_filters.CharFilter(lookup_expr='icontains', label='Razão Social')

    class Meta:
        model = Company
        fields = ['razao_social', 'natureza_juridica', 'porte_empresa']

class MunicipalityFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome do Município')

    class Meta:
        model = Municipality
        fields = ['nome', 'estado']

class DistrictFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome do Distrito')

    class Meta:
        model = District
        fields = ['nome', 'municipio']

class StateFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome do estado')

    regiao = django_filters.ModelChoiceFilter(
        queryset=Region.objects.all(),
        label='Região'
    )

    class Meta:
        model=State
        fields=['nome','regiao']