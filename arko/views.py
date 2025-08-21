from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import State, Municipality, District, Company
from .filters import MunicipalityFilter, CompanyFilter, DistrictFilter, StateFilter

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
        return context
    
def logout_view(request):
    logout(request)

    return redirect('login')