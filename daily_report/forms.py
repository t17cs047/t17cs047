from django import forms
from .models import Activity, DailyReport
from django.contrib.auth import forms as auth_forms

class DailyReportCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = DailyReport
        fields = ("date",)        
ActivityFormset = forms.inlineformset_factory(DailyReport, Activity, fields = '__all__', widgets = {'start_time' : forms.TimeInput(format='%H:%M'), 'end_time' : forms.TimeInput(format='%H:%M')},
    extra = 1, max_num = 1, can_delete= False
    )

class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label
