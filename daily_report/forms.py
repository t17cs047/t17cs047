from django import forms
from .models import Activity, DailyReport, Project, Employee
from django.contrib.auth import forms as auth_forms

from random import choice
from django.db.models.query import QuerySet

from daily_report.models import Employee
from django.contrib.auth.forms import UserCreationForm
from django.template.defaultfilters import default

import datetime


class DailyReportCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = DailyReport
        fields = ("date",)
        
       
ActivityFormset = forms.inlineformset_factory(DailyReport, Activity, fields = '__all__', widgets = {'start_time' : forms.TimeInput(format='%H:%M'), 'end_time' : forms.TimeInput(format='%H:%M') },
    extra = 1, max_num = 1, can_delete= False
    )

class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

class UserCreateForm(UserCreationForm):
    pass


class ProfileForm(forms.ModelForm):
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
    cost = forms.IntegerField(
        label= '原価',
        )
    
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'start_date':DateInput(),
            'end_date':DateInput()
            }
    def clean_date(self):
            start_date = self.start_date.get('start_date')
            end_date = self.end_date.get('end_date')
            if end_date <= start_date:
                raise forms.ValidationError('開始日が終了日より早いです')
            return end_date