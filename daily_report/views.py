from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.template.context_processors import request
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Project, Status
from django.views.generic.base import TemplateView
# Create your views here.

def index(request):
    return render(request, 'daily_report/index.html', {})

class ProjectAddView(CreateView):
    model = Project
    fields = ('name', 'order_amount', 'budget',
              'outsourcing_budget', 'start_date',
              'end_date', 'client', 'outsourcing_cost', 'cost')
    template_name = 'daily_report/project_add.html'

    success_url = 'index/'
    
class ProjectEditView(CreateView):
    model = Project    
    fields = ('name', 'order_amount', 'budget',
              'outsourcing_budget', 'start_date',
              'end_date', 'client', 'outsourcing_cost', 'cost')
    template_name = 'daily_report/project_edit.html'   
    success_url = '../index/'
    
class ProjectAddViewWithParameter(UpdateView):
    model = Project    
    fields = ('name', 'order_amount', 'budget',
              'outsourcing_budget', 'start_date',
              'end_date', 'client', 'outsourcing_cost', 'cost')
    template_name = 'daily_report/project_show.html'   
    success_url = '../index/'
    
class ProjectDeleteView(TemplateView):
    model = Project    
    fields = ('name', 'order_amount', 'budget',
              'outsourcing_budget', 'start_date',
              'end_date', 'client', 'outsourcing_cost', 'cost')
    template_name = 'daily_report/project_delete.html'   
    success_url = '../index/'
    
class WageAddView(CreateView):
    model = Status
    fields = ('name', 'wage')
    template_name = 'daily_report/wage_add.html'

    success_url = 'index/'
    
class CostView(ListView):
    model = Project
    fields = ('name', 'cost')
    template_name = 'daily_report/cost_show.html'

    success_url = 'index/'