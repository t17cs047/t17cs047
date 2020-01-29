from django.shortcuts import render, redirect
from .forms import DailyReportCreateForm, ActivityFormset
from .models import Status, Employee, Project, Activity, DailyReport
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib import messages
from django.views.generic import DetailView
from django.db import transaction
from .forms import ProfileForm, UserCreateForm
from django.views.generic import ListView

from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from daily_report.forms import Project, ProjectBuy, ProjectForm, StatusIdForm, StatusForm, DateInput

from . forms import ProjectForm, ProjectIDForm

from django.template.context_processors import request
from django.db import models
from django.contrib import messages
from django.http.response import HttpResponseForbidden
from django.urls.base import resolve

from django.db import IntegrityError
from decimal import Decimal, ROUND_HALF_UP


# Create your views here.
@login_required
def add_daily_report(request):
    form = DailyReportCreateForm(request.POST or None)
    context = {'form': form}
    me = Employee.objects.get(user = request.user)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        #employee = Employee.objects.get(user = request.user)   
        formset = ActivityFormset(request.POST, instance=post)
        
        if formset.is_valid() and formset.has_changed():
            try:
                post.save() 
                detail = formset.save(commit = False)
                for inform in detail:
                    stime = inform.start_time.hour * 60 + inform.start_time.minute
                    etime = inform.end_time.hour * 60 + inform.end_time.minute
                    inform.time = etime - stime
                formset.save()                
                return redirect('index')
            except IntegrityError:
                return redirect("not_unique")
        
        else:
            context['formset'] = formset
            for form in context['formset']:
                form.fields['project'].queryset =  Project.objects.filter(employee = me)
            #messages.warning(request, "正確に入力してください")
            context['user_name'] = me.name
    else:
        employee = Employee.objects.get(user = request.user)    
        context['formset'] = ActivityFormset()
        for form in context['formset']:
            form.fields['project'].queryset =  Project.objects.filter(employee = employee)
        context['user_name'] = me.name
    return render(request, 'daily_report/daily_report.html', context)

class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    template_name = 'daily_report/activity_delete.html'
    success_url = '../report_list'

 
class AggregateView(LoginRequiredMixin, TemplateView):
    model = Activity
    template_name = 'daily_report/show_cost.html'
    def post(self, request, *args, **kwargs):
        project_id = self.request.POST.get('project_id')
        project = Project.objects.get(pk=project_id)
        context = super().get_context_data(**kwargs)        
        context['form_id'] = ProjectIDForm()        
        employees = project.employee.all()
        sum =0
        for employee in employees:
            #add date__gte 1/22
            daily_reports = DailyReport.objects.filter(user = employee.user, date__lte = project.end_date, date__gte = project.start_date)
            for daily_report in daily_reports:
                activities = Activity.objects.filter(daily_report = daily_report)
                for activity in activities:
                    sum += activity.time * employee.status.wage / 60
        
        aggr = Decimal(str(sum))
        calc = aggr.quantize(Decimal('0'), rounding = ROUND_HALF_UP)

        context['sum'] = calc
        
        ####
        context['project'] = project
        
        ######
        return self.render_to_response(context)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_id'] = ProjectIDForm()
        return context
    
class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = DailyReport
    template_name = 'daily_report/report_delete.html'
    success_url = '../report_list'    

class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "../templates/registration/login.html"

class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "../templates/registration/logout.html"

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

"""12/20"""

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == user.is_superuser




class ReportMixin(object):
    def form_valid(self, form, formset):
        # formset.saveでインスタンスを取得できるように、既存データに変更が無くても更新対象となるようにする
        for detail_form in formset.forms:
            if detail_form.cleaned_data:
                detail_form.has_changed = lambda: True

        # インスタンスの取得
        invoice = form.save(commit=False)
        formset.instance = invoice

        # DB更新
        try:
            with transaction.atomic():
                invoice.save()
                formset.instance = invoice
                detail = formset.save(commit = False)
                for inform in detail:
                    stime = inform.start_time.hour * 60 + inform.start_time.minute
                    etime = inform.end_time.hour * 60 + inform.end_time.minute
                    inform.time = etime - stime
                formset.save()
        except:
            return redirect("not_unique")
        # 処理後は詳細ページを表示
        return redirect("report_list")



class FormsetMixin(object):
    object = None

    def get(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        if getattr(self, 'is_update_view', False):
            self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset_class = self.get_formset_class()
        formset = self.get_formset(formset_class)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_formset_class(self):
        return self.formset_class

    def get_formset(self, formset_class):
        return formset_class(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
            'instance': self.object
        }
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
            })
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return redirect(self.object.get_absolute_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))




class ReportUpdateView(LoginRequiredMixin, ReportMixin, FormsetMixin, UpdateView):
    is_update_view = True
    template_name = 'daily_report/report_edit.html'
    model = DailyReport
    form_class = DailyReportCreateForm
    formset_class = ActivityFormset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = Employee.objects.get(user = self.request.user)
        for form in context['formset']:
            form.fields['project'].queryset =  Project.objects.filter(employee = employee)
        context['user_name'] = employee.name
        return context
    
    
    
@staff_member_required    
def register_user(request):
    user_form = UserCreateForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if request.method == "POST" and user_form.is_valid() and profile_form.is_valid():
        # Userモデルの処理。ログインできるようis_activeをTrueにし保存
        user = user_form.save(commit=False)
        user.is_active = True
        user.save()

        # Profileモデルの処理。↑のUserモデルと紐づけましょう。
        profile = profile_form.save(commit=False)
        profile.user = user
        profile.save()
        return redirect("index")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, 'daily_report/user_create.html', context)    
"""12/20"""


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "daily_report/index.html"

class NotUniqueView(LoginRequiredMixin, TemplateView):
    template_name = "daily_report/not_unique.html"
    
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
        selected_employees = self.request.POST.getlist("employee")
        employee_list = []
        for employee in selected_employees:
            employee_list.append(Employee.objects.get(pk = employee))
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'daily_report/project_show.html', {'form':form, 'employees':employee_list})
        if self.request.POST.get('next', '') == 'create':
            form.save()
            #form.save_m2m()
            return super().form_valid(form)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'daily_report/project_add.html', {'form':form})
        
    
 
    
class ProjectEditViewWithParameter(LoginRequiredMixin, UpdateView):
    model = Project    
    form_class = ProjectForm
    template_name = 'daily_report/project_edit.html'
    success_url = reverse_lazy('list')
    
class ProjectDeleteViewWithParameter(LoginRequiredMixin,DeleteView):
    model = Project 
    template_name = 'daily_report/project_delete.html'   
    success_url = '../list'
    
    def delete(self, request, *args, **kwargs):
        try:
            return super(ProjectDeleteViewWithParameter, self).delete(
                    request, *args, **kwargs
                )
        except models.ProtectedError as e:
            return redirect('project_delete_error')
        
class ProjectDeleteErrorView(LoginRequiredMixin,TemplateView):
    template_name = 'daily_report/project_delete_error.html'       

    
class ProjectDetailViewWithParameter(LoginRequiredMixin, DetailView):
    model = Project    
    template_name = 'daily_report/project_detail.html'
    success_url = '../list'
    
           
class WageList(LoginRequiredMixin, ListView):
    model = Status
    template_name = "status_list.html"  
    def post(self, request, *args, **kwargs):
        status_id = self.request.POST.get('status_id')
        status = get_object_or_404(Status, pk=status_id)
        return HttpResponseRedirect(reverse('list_wage'))
  
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['form'] = StatusIdForm()
       return context


class WageAddView(LoginRequiredMixin, CreateView):
    model = Status
    #fields = ('name', 'wage')
    template_name = 'daily_report/wage_add.html'
    #form_class = forms.ProfileForm
   # success_url = 'daily_report/wage_add.html'
    
    form_class = StatusForm
    #template_name = 'daily_report/project_add.html'  
    success_url = reverse_lazy('list_wage')
    
    def form_valid(self, form):
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'daily_report/wage_show.html', {'form':form})
        if self.request.POST.get('next', '') == 'create':
            #form.save()
            #form.save_m2m()
            return super().form_valid(form)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'daily_report/wage_add.html', {'form':form})
        

        
        
        
               
        
        
class WageEditViewWithParameter(LoginRequiredMixin, UpdateView):
    model = Status  
    fields = ('name', 'wage')
    template_name = 'daily_report/wage_edit.html'
    success_url = reverse_lazy('list_wage')
    
class WageDeleteViewWithParameter(LoginRequiredMixin,DeleteView):
    model = Status
    template_name = 'daily_report/wage_delete.html'   
    success_url = '../list_wage'
    
    def delete(self, request, *args, **kwargs):
        try:
            return super(WageDeleteViewWithParameter, self).delete(
                    request, *args, **kwargs
                )
        except models.ProtectedError as e:
            return redirect('wage_delete_error')
 
class WageDeleteErrorView(LoginRequiredMixin,TemplateView):
    template_name = 'daily_report/wage_delete_error.html'       
    
    
class WageDetailViewWithParameter(LoginRequiredMixin, DetailView):
    model = Status  
    template_name = 'daily_report/wage_detail.html'
    

    
class CostView(LoginRequiredMixin, ListView):
    model = Project
    fields = ('name', 'cost')
    template_name = 'daily_report/cost_show.html'

    success_url = 'index/'
    
    
class EmployeeView(LoginRequiredMixin, ListView):
    model = Employee    
    template_name = "daily_report/worker_list.html"  
    
class EmployeeEditView(UpdateView):
    model = Employee    
    form_class = ProfileForm
    template_name = 'daily_report/worker_edit.html'
    success_url = reverse_lazy('worker_list')
    
class EmployeeDeleteView(DeleteView):
    model = User
    template_name = 'daily_report/worker_delete.html'
    success_url = '../worker_list'
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['employee'] = Employee.objects.get(pk = self.kwargs['pk'])
       return context
