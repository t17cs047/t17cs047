from django.urls import path
from . import views
from daily_report.views import WageAddView, CostView, ProjectList,ProjectDeleteViewWithParameter, ProjectAddView, ProjectEditViewWithParameter, ProjectDetailViewWithParameter, ActivityDeleteView, ReportDeleteView, NotUniqueView

appname = 'daily_report'
urlpatterns = [
        path('daily_report/', views.add_daily_report, name = 'write' ),
        path('login/', views.MyLoginView.as_view(), name="login"),
        path('logout/', views.MyLogoutView.as_view(), name="logout"),
        path('index/',views.IndexView.as_view(), name="index"),
        path("not_unique/", views.NotUniqueView.as_view(), name = "not_unique"),
        path('delete_activity/<int:pk>', views.ActivityDeleteView.as_view(), name = "delete_activity"),
        path('report_list/',views.ListReportView.as_view(), name="report_list"),
        path('activity_list/<int:pk>',views.ActivityListView.as_view(), name="activity_list"),
        path('report_edit/<int:pk>', views.ReportUpdateView.as_view() , name = "report_edit"),
        path('register/', views.register_user, name = "register"),
        path('report_delete/<int:pk>', views.ReportDeleteView.as_view(), name = "report_delete"),
        path('list', ProjectList.as_view(),name='list'),
        path('add', views.ProjectAddView.as_view(), name='add'),
        path('edit/<int:pk>', views.ProjectEditViewWithParameter.as_view(), name='edit_para'),
        path('delete/<int:pk>', ProjectDeleteViewWithParameter.as_view(), name='delete_para'),
        path('detail/<int:pk>', views.ProjectDetailViewWithParameter.as_view(), name='detail'),
        path('add_wage', WageAddView.as_view(), name='add_wage'),
        path('show_cost', CostView.as_view(), name='show_cost'),
  
    ]