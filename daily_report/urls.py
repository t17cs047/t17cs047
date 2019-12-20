from django.urls import path
from . import views

appname = 'daily_report'
urlpatterns = [
        path('daily_report/', views.add_daily_report, name = 'write' ),
        path('login/', views.MyLoginView.as_view(), name="login"),
        path('logout/', views.MyLogoutView.as_view(), name="logout"),
        path('index/',views.IndexView.as_view(), name="index"),
        path('report_list/',views.ListReportView.as_view(), name="report_list"),
        path('activity_list/<int:pk>',views.ActivityListView.as_view(), name="activity_list"),
        path('report_edit/<int:pk>', views.ReportUpdateView.as_view() , name = "report_edit"),
        
    ]