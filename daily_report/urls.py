from django.urls import path
from . import views
from daily_report.views import WageAddView, CostView, ProjectList,ProjectDeleteViewWithParameter, ProjectAddView, ProjectEditView, ProjectEditViewWithParameter, ProjectDeleteView

appname = 'daily_report'
urlpatterns = [
        path('daily_report/', views.add_daily_report, name = 'write' ),
        path('login/', views.MyLoginView.as_view(), name="login"),
        path('logout/', views.MyLogoutView.as_view(), name="logout"),
        path('index/',views.IndexView.as_view(), name="index"),
  
        path('report_list/',views.ListReportView.as_view(), name="report_list"),
        path('activity_list/<int:pk>',views.ActivityListView.as_view(), name="activity_list"),
        path('report_edit/<int:pk>', views.ReportUpdateView.as_view() , name = "report_edit"),
        path('register/', views.register_user, name = "register"),
        
        path('list', ProjectList.as_view(),name='list'),
        path('add', views.ProjectAddView.as_view(), name='add'),
        path('edit/<int:pk>', ProjectEditViewWithParameter.as_view(), name='edit_para'),
        path('delete/<int:pk>', ProjectDeleteViewWithParameter.as_view(), name='delete_para'),
        path('add_wage', WageAddView.as_view(), name='add_wage'),
        path('show_cost', CostView.as_view(), name='show_cost'),
        #path('add/', views.project_create, name='add'),
  
    ]