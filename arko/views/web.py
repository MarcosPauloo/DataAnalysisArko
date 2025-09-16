import json
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.serializers import serialize
from ..models import State, Municipality, District, Company
from ..filters import MunicipalityFilter, CompanyFilter, DistrictFilter, StateFilter

class StateListView(LoginRequiredMixin,ListView):
    model = State
    template_name = 'arko/state_list.html'
    context_object_name = 'states'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('regiao')
        self.filter=StateFilter(self.request.GET, queryset=queryset)
        return self.filter.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        
        paginator = context['paginator']
        page_obj = context['page_obj']

        states_list = list(page_obj.object_list.values('id', 'nome', 'sigla', 'regiao__nome'))
        
        initial_data = {
            "count": paginator.count,
            "next": page_obj.next_page_number() if page_obj.has_next() else None,
            "previous": page_obj.previous_page_number() if page_obj.has_previous() else None,
            "results": states_list
        }

        context['data_json'] = json.dumps(initial_data)

        return context

class MunicipalityListView(LoginRequiredMixin,ListView):
    model = Municipality
    template_name = 'arko/municipality_list.html'
    context_object_name = 'municipalities'
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset().select_related('estado')

        self.filter = MunicipalityFilter(self.request.GET, queryset=queryset)

        return self.filter.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter

        # -- INJEÇÃO DE DADOS PARA O VUE.JS
        municipality_list = list(self.filter.qs.values('id', 'nome', 'estado__nome'))
        context['data_json'] = json.dumps(municipality_list)
        return context
    
class DistrictListView(LoginRequiredMixin,ListView):
    model = District
    template_name = 'arko/district_list.html'
    context_object_name = 'districts'
    paginate_by = 25

    def get_queryset(self):
        query_set = super().get_queryset().select_related('municipio__estado')
        self.filter = DistrictFilter(self.request.GET, queryset=query_set)
        return self.filter.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter

        # -- INJEÇÃO DE DADOS PARA O VUE.JS
        district_list = list(self.filter.qs.values('id', 'nome', 'municipio__nome', 'municipio__estado__nome'))
        context['data_json'] = json.dumps(district_list)

        return context
    
class CompanyListView(LoginRequiredMixin,ListView):
    model = Company
    template_name = 'arko/company_list.html'
    context_object_name = 'companies'
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = CompanyFilter(self.request.GET, queryset=queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter

        context['data_json'] = serialize('json', self.filter.qs, fields=('cnpj', 'razao_social', 'porte_empresa'))

        return context
    
def logout_view(request):
    logout(request)

    return redirect('login')
