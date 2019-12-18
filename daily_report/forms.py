from django import forms
from .models import Activity, DailyReport, Project
from django.contrib.auth import forms as auth_forms

class DailyReportCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = DailyReport
        fields = ("date",)        
ActivityFormset = forms.inlineformset_factory(DailyReport, Activity, fields = '__all__', 
    extra = 1, max_num = 5, can_delete= False
    )

class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

class ProjectBuy(forms.Form):
    project_id = forms.IntegerField(label='ID')
    #project_status=forms.ChoiceField(label='STATUS',widgets=forms.Select,choices=())
    
class ProjectIdForm(forms.Form):
    project_id = forms.IntegerField(label='ID')

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'order_amount', 'budget',
              'outsourcing_budget', 'start_date',
              'end_date', 'client', 'outsourcing_cost', 'cost']
   