from django.shortcuts import render, redirect
from .forms import DailyReportCreateForm, ActivityFormset
from .models import Status, Employee, Project, Activity, DailyReport
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib import messages

from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from daily_report.forms import Project, ProjectBuy, ProjectForm
from . forms import ProjectForm

# Create your views here.
@login_required
def add_daily_report(request):
    form = DailyReportCreateForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        formset = ActivityFormset(request.POST, files=request.FILES, instance=post) 
        if formset.is_valid() and formset.has_changed():
            print("valid")
            post.save()
            formset.save()
            return redirect('index')
        
        else:
            print("else")
            context['formset'] = formset
            messages.warning(request, "fill in the forms correctly!")

    else:
        print("else2")        
        context['formset'] = ActivityFormset()

    return render(request, 'daily_report/daily_report.html', context)



class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "../templates/registration/login.html"

class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "../templates/registration/logout.html"

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "daily_report/index.html"

class ListReportView(LoginRequiredMixin, ListView):
    model = DailyReport
    template_name = "daily_report/report_list.html"
    def get_queryset(self):
        return DailyReport.objects.filter( user = self.request.user)
    
class ActivityListView(LoginRequiredMixin, ListView):
    model = Activity 
    template_name = "daily_report/activity_list.html"
    def get_queryset(self, **kwargs):
        report = get_object_or_404(DailyReport, pk=self.kwargs['pk'])
        return Activity.objects.filter(daily_report = report)
    
'''class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "daily_report/index.html"
'''    
    
class ProjectList(LoginRequiredMixin, ListView):
    model = Project
   
    def post(self, request, *args, **kwargs):
        project_id = self.request.POST.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        return HttpResponseRedirect(reverse('list'))
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProjectBuy()
        return context
    

class ProjectAddView(LoginRequiredMixin,FormView):  
    model = Project
    form_class = ProjectForm
    template_name = 'daily_report/project_add.html'  
    success_url = reverse_lazy('list')
    
    def form_valid(self, form):
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'daily_report/project_show.html', {'form':form})
        if self.request.POST.get('next', '') == 'create':
            form.save()
            return super().form_valid(form)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'daily_report/project_add.html', {'form':form})
        
    
class ProjectEditView(LoginRequiredMixin, UpdateView):
    model = Project    
    form_class = ProjectForm
    template_name = 'daily_report/project_edit.html'   
    success_url =reverse_lazy('list')
    
    def form_valid(self, form):
        if self.request.POST.get('next', '') == 'create':
            form.save()
            return super().form_valid(form)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'daily_report/project_edit.html', {'form':form})
        
    
    
class ProjectEditViewWithParameter(LoginRequiredMixin, UpdateView):
    model = Project    
    form_class = ProjectForm
    template_name = 'daily_report/project_edit.html'
    success_url = reverse_lazy('list')
    
    '''def form_valid(self, form):
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'daily_report/project_edit_confirm.html', {'form':form})
        if self.request.POST.get('next', '') == 'create':
            form.save()
            return super().form_valid(form)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'daily_report/project_edit.html', {'form':form})
      '''  
    
class ProjectDeleteView(LoginRequiredMixin, TemplateView):
    model = Project    
    form_class = ProjectForm
    template_name = 'daily_report/project_delete.html'   
    success_url = '../list'
    
class ProjectDeleteViewWithParameter(LoginRequiredMixin,DeleteView):
    model = Project 
    template_name = 'daily_report/project_delete.html'   
    success_url = '../list'
    
class ProjectDetailViewWithParameter(LoginRequiredMixin, DetailView):
    model = Project    
    template_name = 'daily_report/project_detail.html'
    
    
class WageAddView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ('name', 'wage')
    template_name = 'daily_report/wage_add.html'

    success_url = 'index/'
    
class CostView(LoginRequiredMixin, ListView):
    model = Project
    fields = ('name', 'cost')
    template_name = 'daily_report/cost_show.html'

    success_url = 'index/'
