from django import forms
from .models import Activity, DailyReport, Project, Employee
from django.contrib.auth import forms as auth_forms

from random import choice
from django.db.models.query import QuerySet

from daily_report.models import Employee
from django.contrib.auth.forms import UserCreationForm
from django.template.defaultfilters import default

import datetime
from setuptools.command.setopt import option_base

class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

class UserCreateForm(UserCreationForm):
    pass


class ProfileForm(forms.ModelForm):
    employee = forms.ModelMultipleChoiceField(queryset = Employee.objects.all(),
                                         required = False,
                                         widget = forms.CheckboxSelectMultiple)    
    class Meta:
        model = Employee
        fields = (
            "name", "status", 
        )

class ProjectBuy(forms.Form):
    project_id = forms.IntegerField(label='ID')
    #project_status=forms.ChoiceField(label='STATUS',widgets=forms.Select,choices=())
    
class ProjectIdForm(forms.Form):
    project_id = forms.IntegerField(label='ID')
    
class DateInput(forms.DateInput):
    input_type = 'date'

class ProjectForm(forms.ModelForm):
    employee = forms.ModelMultipleChoiceField(queryset = Employee.objects.all(),
                                         label = 'メンバー社員',
                                         required = False,
                                         widget = forms.CheckboxSelectMultiple)
    
    name = forms.CharField(
        label='プロジェクト名',
        widget = forms.TextInput()
        )
    order_amount = forms.IntegerField(
        label= '受注金額',
        )
    budget = forms.IntegerField(
        label= '予算',
        )
    outsourcing_budget = forms.IntegerField(
        label= '外注費予算',
        )
    client = forms.CharField(
        label='顧客名',
        widget = forms.TextInput()
        )
    outsourcing_cost = forms.IntegerField(
        label= '外注費',
        )
    
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'start_date':DateInput(),
            'end_date':DateInput()
            }
        
    def clean(self):
            clean_date = super(ProjectForm, self).clean()
            start_date = clean_date.get('start_date')
            end_date = clean_date.get('end_date')
            if end_date < start_date:
                raise forms.ValidationError('終了日が開始日より早いです')
            return clean_date

class ProjectIDForm(forms.Form):
    project_id = forms.ModelChoiceField(queryset = Project.objects.all(), label = "Project")


        
class StatusIdForm(forms.Form):
    status_id = forms.IntegerField(label='ID')

class DailyReportCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = DailyReport
        fields = ("date",)
        widgets = {
            'date':DateInput(),
            }           
   
       
ActivityFormset = forms.inlineformset_factory(DailyReport, Activity, fields = ('start_time','end_time','daily_report','project','memo'), widgets = {'start_time' : forms.TimeInput(format='%H:%M'), 'end_time' : forms.TimeInput(format='%H:%M')},
    extra = 1, max_num = 1, can_delete= True
    )
#'start_time','end_time','daily_report','project','memo'


