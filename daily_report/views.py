from django.shortcuts import render, redirect
from .forms import DailyReportCreateForm, ActivityFormset
from .models import Status, Employee, Project, Activity, DailyReport
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib import messages
from django.shortcuts import get_object_or_404
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
    