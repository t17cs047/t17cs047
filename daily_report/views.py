from django.shortcuts import render, redirect
from .forms import DailyReportCreateForm, ActivityFormset
from .models import Status, Employee, Project, Activity, DailyReport
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
from django.shortcuts import get_object_or_404
from django.db import transaction
from .forms import ProfileForm, UserCreateForm
# Create your views here.
@login_required
def add_daily_report(request):
    form = DailyReportCreateForm(request.POST or None)
    context = {'form': form}
    print("call1")

   # for project in Project.objects.all():
       # if(project.member.user == request.user):
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        employee = Employee.objects.get(user = request.user)   
        formset = ActivityFormset(request.POST, instance=post)
        
        if formset.is_valid() and formset.has_changed():
            print("valid")
            post.save()
            formset.save()
            return redirect('index')
        
        else:
            print("else")
            context['formset'] = formset
            for form in context['formset']:
                form.fields['project'].queryset =  Project.objects.filter(member = employee)
            messages.warning(request, "fill in the forms correctly!")

    else:
        employee = Employee.objects.get(user = request.user)    
        context['formset'] = ActivityFormset()
        for form in context['formset']:
            form.fields['project'].queryset =  Project.objects.filter(member = employee)
        print(Project.objects.filter(member = employee)) 
        
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
        with transaction.atomic():
            invoice.save()
            formset.instance = invoice
            formset.save()

        # 処理後は詳細ページを表示
        print("valid1")
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
                'files': self.request.FILES,
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


