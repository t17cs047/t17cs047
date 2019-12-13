from django.db import models
from datetime import datetime
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
    
    date = models.DateField(verbose_name = "日付", default = datetime.now)        
    
class Activity(models.Model):
    class Meta:
        db_table = "activity"
    
    start_time = models.DateTimeField(verbose_name = "日付", default = datetime.now)
    end_time = models.DateTimeField(verbose_name = "日付", default = datetime.now)    
    daily_report = models.ForeignKey(DailyReport, on_delete = models.PROTECT)

class Project(models.Model):
    class Meta:
        db_table = "project"
    name = models.CharField(max_length = 30, unique = True)
    order_amount = models.IntegerField()
    budget = models.IntegerField()
    outsourcing_budget = models.IntegerField()
    start_date = models.DateField(verbose_name = "日付", default = datetime.now)
    end_date = models.DateField(verbose_name = "日付", default = datetime.now)
    client = models.CharField(max_length = 30)
    outsourcing_cost = models.IntegerField() 
    cost = models.IntegerField()
      
    
    def __str__(self):
        return self.name


class Employee(models.Model):
    class Meta:
        db_table = "employee"
    
    name = models.CharField(max_length = 100)
    status = models.ForeignKey(Status, on_delete = models.PROTECT )
    project = models.ManyToManyField(Project)
    daily_report = models.ForeignKey(DailyReport, on_delete = models.PROTECT)
    
    def __str__(self):
        return self.name    

class SumTime():
    class Meta:
        db_table = "sum"
        
    project = models.ForeignKey(Project, on_delete = models.PROTECT )
    
    
# Create your models here.
