from django.urls import path
from . import views
from daily_report.views import WageAddView, WageList
from django.contrib.admin.views.decorators import staff_member_required

appname = 'daily_report'
urlpatterns = [
    path('add', staff_member_required(views.ProjectAddView.as_view()), name='add'),
       path('daily_report/', views.add_daily_report, name = 'write' ),
        path('login/', views.MyLoginView.as_view(), name="login"),
        path('logout/', views.MyLogoutView.as_view(), name="logout"),
        path('index/',views.IndexView.as_view(), name="index"),
        path('register/', views.register_user, name = "register"),
        path('list_wage/', staff_member_required(views.WageList.as_view()),name='list_wage'),
        path('wage_edit/<int:pk>', staff_member_required(views.WageEditViewWithParameter.as_view()), name='wage_edit_para'),
        path('wage_delete/<int:pk>', staff_member_required(views.WageDeleteViewWithParameter.as_view()), name='wage_delete_para'),
        path('wage_delete_error', staff_member_required(views.WageDeleteErrorView.as_view()), name='wage_delete_error'),
        path('wage_detail/<int:pk>', staff_member_required(views.WageDetailViewWithParameter.as_view()), name='wage_detail'),
        path('add_wage', staff_member_required(WageAddView.as_view()), name='add_wage'),
        path('worker_list', staff_member_required(views.EmployeeView.as_view()), name = 'worker_list'),
      
        path('edit_woker/<int:pk>', staff_member_required(views.EmployeeEditView.as_view()), name='edit_worker'),
        path('delete_woker/<int:pk>', staff_member_required(views.EmployeeDeleteView.as_view()), name='delete_worker'),
  
    ]

"""
 path("not_unique/", views.NotUniqueView.as_view(), name = "not_unique"),
 path('delete_activity/<int:pk>', views.ActivityDeleteView.as_view(), name = "delete_activity"),
path('activity_list/<int:pk>',views.ActivityListView.as_view(), name="activity_list"),
path('report_edit/<int:pk>', views.ReportUpdateView.as_view() , name = "report_edit"),
path('report_delete/<int:pk>', views.ReportDeleteView.as_view(), name = "report_delete"),
path('list', staff_member_required(ProjectList.as_view()),name='list'),
path('edit/<int:pk>', staff_member_required(views.ProjectEditViewWithParameter.as_view()), name='edit_para'),
path('delete/<int:pk>', staff_member_required(ProjectDeleteViewWithParameter.as_view()), name='delete_para'),
    path('project_delete_error', staff_member_required(views.ProjectDeleteErrorView.as_view()), name='project_delete_error'),
    path('detail/<int:pk>', staff_member_required(views.ProjectDetailViewWithParameter.as_view()), name='detail'),
      path('show_cost', staff_member_required(AggregateView.as_view()), name='show_cost'),
       path('report_list/',views.ListReportView.as_view(), name="report_list"),
"""      