from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

from pip.cmdoptions import verbose

from django.conf import settings

# Create your models here.
class Status(models.Model):
    class Meta:
        db_table = "status"
        
    name = models.CharField(max_length = 100,unique = True)
    wage = models.IntegerField()
    
    def __str__(self):
        return self.name
    
class DailyReport(models.Model):
    class Meta:
        db_table = "daily_report"
        unique_together = ('date', 'user')
    
    date = models.DateField(verbose_name = "日付", default = datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)   

class Employee(models.Model):
    class Meta:
        db_table = "employee"
    
    name = models.CharField(max_length = 100)
    status = models.ForeignKey(Status, on_delete = models.PROTECT )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Project(models.Model):
    class Meta:
        db_table = "project"
    name = models.CharField(max_length = 30, unique = True)
    employee = models.ManyToManyField(Employee)
    order_amount = models.IntegerField()
    budget = models.IntegerField()
    outsourcing_budget = models.IntegerField()
    start_date = models.DateField(verbose_name = "日付", default = datetime.now)
    end_date = models.DateField(verbose_name = "日付", default = datetime.now)
    client = models.CharField(max_length = 30)
    outsourcing_cost = models.IntegerField() 
    
    def __str__(self):
        return self.name

class Activity(models.Model):
    class Meta:
        db_table = "activity"
    
    start_time = models.TimeField(verbose_name = "開始時間", default = datetime.now)
    end_time = models.TimeField(verbose_name = "終了時間", default = datetime.now)    
    daily_report = models.ForeignKey(DailyReport, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete = models.PROTECT, verbose_name='プロジェクト')
    memo = models.CharField(max_length = 100,  verbose_name='備考')
    time = models.IntegerField(default = 0)
    
class SumTime():
    class Meta:
        db_table = "sum"
        
    project = models.ForeignKey(Project, on_delete = models.PROTECT )
    
